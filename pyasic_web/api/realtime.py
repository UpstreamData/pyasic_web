import asyncio

from fastapi import APIRouter, WebSocket
import websockets
import websockets.exceptions
from fastapi.websockets import WebSocketDisconnect

import pyasic
from pyasic.misc import Singleton
from pyasic_web.func import get_current_miner_list
from pyasic_web.func import get_user_ip_range
from pyasic_web.func.auth import ws_login_req
from pyasic_web.func.web_settings import (
    get_current_settings,
)
import json
from pyasic_web.errors.miner import MinerDataError


router = APIRouter(prefix="/realtime")

class MinerDataManager(metaclass=Singleton):
    def __init__(self):
        self.data = {}
        self.miners = []
        self._publish = asyncio.Event()

    async def run(self):
        graph_sleep_time = get_current_settings()["graph_data_sleep_time"]
        while True:
            self.miners = await get_current_miner_list()
            d = await asyncio.gather(*[get_miner_data(m) for m in self.miners])
            self.data = {str(i["ip"]): i for i in d}
            await self.publish()
            await asyncio.sleep(graph_sleep_time)

    async def publish(self):
        self._publish.set()
        await asyncio.sleep(0) # yield to event loop
        self._publish.clear()

    async def subscribe(self):
        if not self.data == {}:
            yield self.data
        while True:
            await self._publish.wait()
            yield self.data
            await asyncio.sleep(0) # yield to event loop

    async def subscribe_to_updates(self):
        if not self.data == {}:
            yield True
        while True:
            await self._publish.wait()
            yield True
            await asyncio.sleep(0) # yield to event loop

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

users = {}
pool_data = [dp.get("pool_1_user") for dp in users]
for user in pool_data: # data
    if user:
        if not user in users:
            users[user] = 0
        users[user] += 1

@router.websocket("/all")
async def all_data(websocket: WebSocket):
    await ws_login_req(websocket)
    await websocket.accept()
    data_manager = MinerDataManager()
    irange = await get_user_ip_range(websocket)
    allowed_miners = await get_current_miner_list(irange)
    async for data in data_manager.subscribe():
        try:
            await websocket.send_json(
                {d: data[d] for d in data if d in allowed_miners}
            )
        except WebSocketDisconnect:
            print("Websocket disconnected.")
            return
        except websockets.exceptions.ConnectionClosedError:
            print("Websocket disconnected.")
            return
        except websockets.exceptions.ConnectionClosedOK:
            return


@router.websocket("/updates")
async def all_data(websocket: WebSocket):
    await ws_login_req(websocket)
    await websocket.accept()
    data_manager = MinerDataManager()
    async for update in data_manager.subscribe_to_updates():
        try:
            await websocket.send_json(
                {"update": update}
            )
        except WebSocketDisconnect:
            print("Websocket disconnected.")
            return
        except websockets.exceptions.ConnectionClosedError:
            print("Websocket disconnected.")
            return
        except websockets.exceptions.ConnectionClosedOK:
            return
