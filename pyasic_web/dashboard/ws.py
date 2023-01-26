import asyncio
import datetime
import ipaddress

import websockets.exceptions
from fastapi import WebSocket, WebSocketDisconnect, APIRouter

from pyasic.misc import Singleton
from pyasic_web.func import get_current_miner_list
from pyasic_web._settings.func import (  # noqa - Ignore access to _module
    get_current_settings,
)
from pyasic_web.dashboard.func import get_miner_data_dashboard


router = APIRouter()

class MinerDataManager(metaclass=Singleton):
    def __init__(self):
        self.cached_data = None


@router.websocket("/dashboard/ws")
async def dashboard_websocket(websocket: WebSocket):
    await websocket.accept()
    # while True:
    #     await asyncio.sleep(5)
    graph_sleep_time = get_current_settings()["graph_data_sleep_time"]
    data_manager = MinerDataManager()
    try:
        if data_manager.cached_data:
            await websocket.send_json(
                {
                    "datetime": datetime.datetime.now().isoformat(),
                    "miners": data_manager.cached_data,
                }
            )
        while True:
            miners = get_current_miner_list()
            all_miner_data = []
            data_gen = asyncio.as_completed(
                [get_miner_data_dashboard(miner_ip) for miner_ip in miners]
            )
            for all_data in data_gen:
                data_point = await all_data
                all_miner_data.append(data_point)
            all_miner_data.sort(key=lambda x: ipaddress.ip_address(x["ip"]))
            data_manager.cached_data = all_miner_data
            await websocket.send_json(
                {
                    "datetime": datetime.datetime.now().isoformat(),
                    "miners": all_miner_data,
                }
            )
            await asyncio.sleep(graph_sleep_time)
    except WebSocketDisconnect:
        print("Websocket disconnected.")
        pass
    except websockets.exceptions.ConnectionClosedOK:
        pass
