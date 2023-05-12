# ------------------------------------------------------------------------------
#  Copyright 2022 Upstream Data Inc                                            -
#                                                                              -
#  Licensed under the Apache License, Version 2.0 (the "License");             -
#  you may not use this file except in compliance with the License.            -
#  You may obtain a copy of the License at                                     -
#                                                                              -
#      http://www.apache.org/licenses/LICENSE-2.0                              -
#                                                                              -
#  Unless required by applicable law or agreed to in writing, software         -
#  distributed under the License is distributed on an "AS IS" BASIS,           -
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    -
#  See the License for the specific language governing permissions and         -
#  limitations under the License.                                              -
# ------------------------------------------------------------------------------

import asyncio
import json
from typing import List, Literal, Union, Callable, Type, Dict

import websockets
import websockets.exceptions
from fastapi import APIRouter, WebSocket, Security
from fastapi.websockets import WebSocketDisconnect
from sse_starlette import EventSourceResponse
from starlette.requests import Request

import pyasic
from pyasic.misc import Singleton
from pyasic_web.api.responses import MinerSelector, MinerResponse
from pyasic_web.auth import AUTH_SCHEME
from pyasic_web.auth.users import get_current_user
from pyasic_web.errors.miner import MinerDataError
from pyasic_web.func.miners import get_current_miner_list
from pyasic_web.func.web_settings import get_current_settings

router = APIRouter(prefix="/realtime", dependencies=[Security(AUTH_SCHEME)])

MESSAGE_STREAM_RETRY_TIMEOUT = 15000  # MS


class MinerDataManager(metaclass=Singleton):
    def __init__(self):
        self.data = {}
        self.miners = []
        self._publish = asyncio.Event()

    async def run(self):
        graph_sleep_time = get_current_settings()["data_sleep_time"]
        while True:
            self.miners = await get_current_miner_list()
            d = await asyncio.gather(*[get_miner_data(m) for m in self.miners])
            self.data = {str(i["ip"]): i for i in d}
            await self.publish()
            await asyncio.sleep(graph_sleep_time)

    async def publish(self):
        self._publish.set()
        await asyncio.sleep(0)  # yield to event loop
        self._publish.clear()

    async def subscribe(self):
        if not self.data == {}:
            yield self.data
        while True:
            await self._publish.wait()
            yield self.data
            await asyncio.sleep(0)  # yield to event loop

    async def subscribe_to_updates(self):
        if not self.data == {}:
            yield True
        while True:
            await self._publish.wait()
            yield True
            await asyncio.sleep(0)  # yield to event loop


def get_data_by_selector(
    data_key: str, selector: Union[List[str], str, Literal["all"]]
) -> dict:
    miner_data = MinerDataManager().data
    if selector == "all":
        data = {d: miner_data[d][data_key] for d in miner_data if miner_data[d].get(data_key) is not None}
    else:
        data = {d: miner_data[d][data_key] for d in miner_data if miner_data[d].get(data_key) is not None and d in selector}
    return data

def create_return_by_selector(
    data_key: str, selector: Union[List[str], str, Literal["all"]], ret_type: type(MinerResponse)
) -> Dict[str, type(MinerResponse)]:
    miner_data = MinerDataManager().data
    if selector == "all":
        data = {d: ret_type(value=miner_data[d][data_key]) for d in miner_data if miner_data[d].get(data_key) is not None}
    else:
        data = {d: ret_type(value=miner_data[d][data_key]) for d in miner_data if miner_data[d].get(data_key) is not None and d in selector}
    return data

async def get_miner_data(miner_ip):
    try:
        settings = get_current_settings()
        miner_identify_timeout = settings["miner_identify_timeout"]
        miner_data_timeout = settings["miner_data_timeout"]

        miner = await asyncio.wait_for(
            pyasic.get_miner(miner_ip), miner_identify_timeout
        )

        data = await asyncio.wait_for(miner.get_data(), miner_data_timeout)

        # return {"ip": str(miner_ip.ip), "hashrate": data.hashrate}
        return json.loads(data.as_json())

    except asyncio.exceptions.TimeoutError:
        return {"ip": miner_ip, "py_error": MinerDataError.NO_RESPONSE.value}

    except KeyError:
        return {
            "ip": miner_ip,
            "py_error": MinerDataError.BAD_DATA.value,
        }


@router.websocket("/updates")
async def updates(websocket: WebSocket):
    await websocket.accept()
    data_manager = MinerDataManager()
    async for update in data_manager.subscribe_to_updates():
        try:
            await websocket.send_json({"update": update})
        except WebSocketDisconnect:
            print("Websocket disconnected.")
            return
        except websockets.exceptions.ConnectionClosedError:
            print("Websocket disconnected.")
            return
        except websockets.exceptions.ConnectionClosedOK:
            return


async def event_generator(
    request: Request,
    miner_selector: MinerSelector,
    data: str,
    unit: str,
    parse_func: Callable,
):
    msg_id = 0
    data_manager = MinerDataManager()
    yield {
        "event": "new_message",
        "id": msg_id,
        "retry": MESSAGE_STREAM_RETRY_TIMEOUT,
        "data": MinerResponse(
            value=parse_func(get_data_by_selector(data, miner_selector.miner_selector)),
            unit=unit,
        ),
    }
    async for _ in data_manager.subscribe_to_updates():
        msg_id += 1
        if await request.is_disconnected():
            break
        yield {
            "event": "new_message",
            "id": msg_id,
            "retry": MESSAGE_STREAM_RETRY_TIMEOUT,
            "data": MinerResponse(
                value=parse_func(
                    get_data_by_selector(data, miner_selector.miner_selector)
                ),
                unit=unit,
            ),
        }


@router.post("/hashrate", dependencies=[Security(get_current_user)])
async def hashrate_stream(request: Request, selector: MinerSelector):
    return EventSourceResponse(
        event_generator(
            request,
            selector,
            "hashrate",
            "TH/s",
            lambda x: round(sum(x), 2),
        )
    )
