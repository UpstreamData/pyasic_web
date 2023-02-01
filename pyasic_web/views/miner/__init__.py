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
from pyasic_web.func import get_current_miner_list
from pyasic_web.func.web_settings import (  # noqa - Ignore access to _module
    get_current_settings,
)
from pyasic_web.templates import templates


def page_miner(request: Request):
    miner_ip = request.path_params["miner_ip"]
    return templates.TemplateResponse(
        "miner.html",
        {"request": request, "cur_miners": get_current_miner_list(), "miner": miner_ip},
    )


def page_remove_miner(request: Request):
    miner_ip = request.path_params["miner_ip"]
    miners = get_current_miner_list()
    miners.remove(miner_ip)
    with open(settings.MINER_LIST, "w") as file:
        for miner_ip in miners:
            file.write(miner_ip + "\n")

    return RedirectResponse(request.url_for("page_dashboard"))


async def page_light_miner(request: Request):
    miner_ip = request.path_params["miner_ip"]
    miner = await pyasic.get_miner(miner_ip)
    print(miner.light)
    if miner.light:
        asyncio.create_task(miner.fault_light_off())
    else:
        asyncio.create_task(miner.fault_light_on())

    return RedirectResponse(request.url_for("page_miner", miner_ip=miner_ip))


async def page_wattage_set_miner(request: Request):
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
    miner_ip = websocket.path_params["miner_ip"]
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
                    "max_wattage": data.wattage_limit,
                    "fault_light": data.fault_light,
                    "errors": [err.error_message for err in data.errors],
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
