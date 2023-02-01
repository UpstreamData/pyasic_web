import asyncio
import datetime
import ipaddress

import websockets.exceptions
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.websockets import WebSocketDisconnect

from pyasic.misc import Singleton
from pyasic_web.func import get_current_miner_list
from pyasic_web.func.dashboard import get_miner_data_dashboard, get_pool_users_data
from pyasic_web.func.web_settings import (  # noqa - Ignore access to _module
    get_current_settings,
)
from pyasic_web.templates import templates


class MinerDataManager(metaclass=Singleton):
    def __init__(self):
        self.cached_data = None


def page_dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "cur_miners": get_current_miner_list()}
    )

def redirect_dashboard(request: Request):
    return RedirectResponse(request.url_for("page_dashboard"))

async def ws_dashboard(websocket):
    await websocket.accept()
    # while True:
    #     await asyncio.sleep(5)
    graph_sleep_time = get_current_settings()["graph_data_sleep_time"]
    data_manager = MinerDataManager()
    try:
        miners = get_current_miner_list()
        if len(miners) > 0:
            if data_manager.cached_data:
                pool_users = get_pool_users_data(data_manager.cached_data)
                await websocket.send_json(
                    {
                        "datetime": datetime.datetime.now().isoformat(),
                        "miners": data_manager.cached_data,
                        "pool_users": pool_users,
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
            pool_users = get_pool_users_data(data_manager.cached_data)
            await websocket.send_json(
                {
                    "datetime": datetime.datetime.now().isoformat(),
                    "miners": all_miner_data,
                    "pool_users": pool_users,
                }
            )
            await asyncio.sleep(graph_sleep_time)
    except WebSocketDisconnect:
        print("Websocket disconnected.")
        pass
    except websockets.exceptions.ConnectionClosedOK:
        pass
