import asyncio
import datetime

import websockets.exceptions
from fastapi import WebSocket, WebSocketDisconnect, APIRouter

from pyasic.misc import Singleton
from pyasic.miners.miner_factory import MinerFactory
from pyasic_web._settings.func import (  # noqa - Ignore access to _module
    get_current_settings,
)


router = APIRouter()

class SingleMinerDataManager(metaclass=Singleton):
    def __init__(self):
        self.cached_data = None



@router.websocket("/{miner_ip}/ws")
async def miner_websocket(websocket: WebSocket, miner_ip):
    await websocket.accept()
    settings = get_current_settings()
    miner_identify_timeout = settings["miner_identify_timeout"]
    miner_data_timeout = settings["miner_data_timeout"]
    data_manager = SingleMinerDataManager()
    if data_manager.cached_data:
        await websocket.send_json(data_manager.cached_data)
    try:
        while True:
            try:
                cur_miner = await asyncio.wait_for(
                    MinerFactory().get_miner(str(miner_ip)), miner_identify_timeout
                )
                data = await asyncio.wait_for(cur_miner.get_data(), miner_data_timeout)

                fan_speeds = [
                    fan if not fan == -1 else 0
                    for fan in [data.fan_1, data.fan_2, data.fan_3, data.fan_4]
                ]
                data = {
                    "hashrate": data.hashrate,
                    "fans": fan_speeds,
                    "temp": data.temperature_avg,
                    "datetime": datetime.datetime.now().isoformat(),
                    "model": data.model,
                    "efficiency": data.efficiency,
                    "wattage": data.wattage,
                    "fault_light": data.fault_light,
                    "errors": [
                        err.error_message for err in data.errors
                    ]
                }
                data_manager.cached_data = data
                await websocket.send_json(data)
                await asyncio.sleep(settings["graph_data_sleep_time"])
            except asyncio.exceptions.TimeoutError:
                data = {"errors": ["The miner is not responding."]}
                await websocket.send_json(data)
                await asyncio.sleep(0.5)
            except KeyError as e:
                print(e)
                data = {"errors": ["The miner returned unusable/unsupported data."]}
                await websocket.send_json(data)
                await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        print("Websocket disconnected.")
    except websockets.exceptions.ConnectionClosedOK:
        pass
