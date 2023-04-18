import asyncio
import datetime

import websockets.exceptions
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

import pyasic
from pyasic.miners.miner_factory import MinerFactory
from pyasic.misc import Singleton
from pyasic_web import settings
from pyasic_web.func import get_current_miner_list, get_user_ip_range, get_current_user
from pyasic_web.func.web_settings import (  # noqa - Ignore access to _module
    get_current_settings,
)
from pyasic_web.templates import templates, card_exists
from pyasic_web.func.auth import login_req, ws_login_req
from starlette.exceptions import HTTPException
from pyasic_web.errors.miner import MinerDataError


async def page_miner(request: Request):
    await login_req(request)
    miner_ip = request.path_params["miner_ip"]
    miners = get_current_miner_list(await get_user_ip_range(request))
    if miner_ip not in miners:
        raise HTTPException(403)

    return templates.TemplateResponse(
        "miner.html",
        {
            "request": request,
            "cur_miners": miners,
            "miner": miner_ip,
            "user": await get_current_user(request),
            "card_exists": card_exists,
        },
    )


async def page_remove_miner(request: Request):
    await login_req(request)
    miner_ip = request.path_params["miner_ip"]
    miners = get_current_miner_list("*")
    miners.remove(miner_ip)
    with open(settings.MINER_LIST, "w") as file:
        for miner_ip in miners:
            file.write(miner_ip + "\n")

    return RedirectResponse("/dashboard")


async def page_light_miner(request: Request):
    await login_req(request)
    miner_ip = request.path_params["miner_ip"]
    miner = await pyasic.get_miner(miner_ip)
    if miner.light:
        asyncio.create_task(miner.fault_light_off())
    else:
        asyncio.create_task(miner.fault_light_on())

    return RedirectResponse("/miner/" + miner_ip)


async def page_wattage_set_miner(request: Request):
    await login_req(request)
    miner_ip = request.path_params["miner_ip"]
    d = await request.json()
    wattage = d["wattage"]
    if wattage:
        miner = await pyasic.get_miner(miner_ip)
        await miner.set_power_limit(int(wattage))


class SingleMinerDataManager(metaclass=Singleton):
    def __init__(self):
        self.cached_data = None


async def ws_miner(websocket: WebSocket):
    await ws_login_req(websocket)
    miner_ip = websocket.path_params["miner_ip"]
    await websocket.accept()
    settings = get_current_settings()
    miner_identify_timeout = settings["miner_identify_timeout"]
    miner_data_timeout = settings["miner_data_timeout"]
    data_manager = SingleMinerDataManager()
    try:
        if data_manager.cached_data["ip"] == miner_ip:
            await websocket.send_text(data_manager.cached_data)
    except (TypeError, KeyError):
        pass
    try:
        while True:
            try:
                cur_miner = await asyncio.wait_for(
                    MinerFactory().get_miner(str(miner_ip)), miner_identify_timeout
                )
                data = await asyncio.wait_for(cur_miner.get_data(), miner_data_timeout)
                data = data.as_json()
                data_manager.cached_data = data
                await websocket.send_text(data)
                await asyncio.sleep(settings["graph_data_sleep_time"])
            except asyncio.exceptions.TimeoutError:
                data = {"py_errors": [MinerDataError.NO_RESPONSE.value]}
                await websocket.send_json(data)
                await asyncio.sleep(0.5)
            except KeyError as e:
                print(e)
                data = {"py_errors": [MinerDataError.BAD_DATA.value]}
                await websocket.send_json(data)
                await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        print("Websocket disconnected.")
    except websockets.exceptions.ConnectionClosedOK:
        pass
