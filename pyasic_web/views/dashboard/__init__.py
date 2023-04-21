import asyncio
import datetime
import ipaddress

import websockets.exceptions
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.websockets import WebSocketDisconnect

from pyasic.misc import Singleton
from pyasic_web.templates import card_exists
from pyasic_web.func import get_current_miner_list, get_user_ip_range, get_current_user
from pyasic_web.func.dashboard import get_miner_data_dashboard, get_pool_users_data
from pyasic_web.func.web_settings import (  # noqa - Ignore access to _module
    get_current_settings,
)
from pyasic_web.errors.miner import MinerDataError
from pyasic_web.templates import templates
from pyasic_web.func.auth import login_req, ws_login_req


class MinerDataManager(metaclass=Singleton):
    def __init__(self):
        self.cached_data = None

    def get_cached_data(self, miners: list):
        data_ret = []
        for d in self.cached_data:
            if d["ip"] in miners:
                data_ret.append(d)
        return data_ret


async def page_dashboard(request: Request):
    await login_req(request)
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "cur_miners": await get_current_miner_list(
                await get_user_ip_range(request)
            ),
            "user": await get_current_user(request),
            "card_exists": card_exists,
        },
    )


def redirect_dashboard(request: Request):
    return RedirectResponse("/dashboard")


async def ws_dashboard(websocket):
    await ws_login_req(websocket)
    await websocket.accept()
    # while True:
    #     await asyncio.sleep(5)
    graph_sleep_time = get_current_settings()["data_sleep_time"]
    data_manager = MinerDataManager()
    try:
        irange = await get_user_ip_range(websocket)
        miners = await get_current_miner_list(irange)
        if len(miners) > 0:
            if data_manager.cached_data:
                pool_users = get_pool_users_data(data_manager.cached_data)
                await websocket.send_json(
                    {
                        "datetime": datetime.datetime.now().isoformat(),
                        "miners": data_manager.get_cached_data(
                            await get_current_miner_list(irange)
                        ),
                        "pool_users": pool_users,
                    }
                )
        while True:
            miners = await get_current_miner_list(irange)
            all_miner_data = []
            py_errors = {}
            data_gen = asyncio.as_completed(
                [get_miner_data_dashboard(miner_ip) for miner_ip in miners]
            )
            for all_data in data_gen:
                data_point = await all_data
                if "py_error" in data_point:
                    if data_point["py_error"] in py_errors:
                        py_errors[data_point["py_error"]] += 1
                    else:
                        py_errors[data_point["py_error"]] = 1
                else:
                    all_miner_data.append(data_point)
            py_errors = [
                {"err": item.value, "count": py_errors[item]} for item in py_errors
            ]
            all_miner_data.sort(key=lambda x: ipaddress.ip_address(x["ip"]))
            data_manager.cached_data = all_miner_data
            pool_users = get_pool_users_data(data_manager.cached_data)
            await websocket.send_json(
                {
                    "datetime": datetime.datetime.now().isoformat(),
                    "miners": all_miner_data,
                    "pool_users": pool_users,
                    "py_errors": py_errors,
                }
            )
            await asyncio.sleep(graph_sleep_time)
    except WebSocketDisconnect:
        print("Websocket disconnected.")
        pass
    except websockets.exceptions.ConnectionClosedError:
        print("Websocket disconnected.")
        pass
    except websockets.exceptions.ConnectionClosedOK:
        pass
