import asyncio
import json
from typing import List, Literal, Union

import websockets
import websockets.exceptions
from fastapi import APIRouter, WebSocket
from fastapi.websockets import WebSocketDisconnect
from sse_starlette import EventSourceResponse

import pyasic
from pyasic.misc import Singleton
from pyasic_web.errors.miner import MinerDataError
from pyasic_web.func import get_current_miner_list, get_user_ip_range
from pyasic_web.func.auth import login_req
from pyasic_web.func.web_settings import get_current_settings

from .func import convert_hashrate, get_allowed_miners
from .responses import MinerResponse, MinerSelector

router = APIRouter(prefix="/realtime")


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
):
    miner_data = MinerDataManager().data
    if selector == "all":
        data = [miner_data[d].get(data_key) for d in miner_data]
    else:
        data = [miner_data[d].get(data_key) for d in miner_data if d in selector]
    return list(filter(lambda x: x is not None, data))


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


@login_req()
@router.websocket("/all")
async def all_data(websocket: WebSocket):
    await websocket.accept()
    data_manager = MinerDataManager()
    irange = await get_user_ip_range(websocket)
    allowed_miners = await get_current_miner_list(irange)
    async for data in data_manager.subscribe():
        try:
            await websocket.send_json({d: data[d] for d in data if d in allowed_miners})
        except WebSocketDisconnect:
            print("Websocket disconnected.")
            return
        except websockets.exceptions.ConnectionClosedError:
            print("Websocket disconnected.")
            return
        except websockets.exceptions.ConnectionClosedOK:
            return


@login_req()
@router.websocket("/updates")
async def all_data(websocket: WebSocket):
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
