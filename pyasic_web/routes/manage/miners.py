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

import websockets.exceptions
from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect

from pyasic import get_miner
from pyasic_web import settings
from pyasic_web.api.realtime import MinerDataManager
from pyasic_web.func import (
    get_current_miner_list,
    get_current_user,
    get_user_ip_range,
)
from pyasic_web.func.auth import login_req
from pyasic_web.templates import templates

router = APIRouter()


@router.route("/")
@login_req()
async def manage_miners_page(request: Request):
    return templates.TemplateResponse(
        "manage_miners.html",
        {
            "request": request,
            "cur_miners": await get_current_miner_list(
                await get_user_ip_range(request)
            ),
            "user": await get_current_user(request),
        },
    )


@router.websocket("/ws")
@login_req()
async def manage_miners_ws(websocket: WebSocket):
    await websocket.accept()
    miners = await get_current_miner_list(await get_user_ip_range(websocket))
    try:
        async for data in MinerDataManager().subscribe():
            for miner in miners:
                if miner in data:
                    await websocket.send_text(json.dumps(data[miner]))
    except WebSocketDisconnect:
        print("Websocket disconnected.")
    except websockets.exceptions.ConnectionClosedOK:
        pass


@router.route("/light", methods=["POST"])
@login_req()
async def manage_miners_light_page(request: Request):
    miners_light = (await request.json())["miners"]
    if not miners_light:
        return RedirectResponse(request.url_for("manage_miners_page"), status_code=303)
    miners = await asyncio.gather(*[get_miner(miner) for miner in miners_light])
    lights = await asyncio.gather(*[miner.check_light() for miner in miners])
    tasks = []
    for idx, miner in enumerate(miners):
        if lights[idx]:
            tasks.append(miner.fault_light_off())
        else:
            tasks.append(miner.fault_light_on())
    await asyncio.gather(*tasks)
    return RedirectResponse(request.url_for("manage_miners_page"), status_code=303)


@router.route("/reboot", methods=["POST"])
@login_req()
async def manage_miners_reboot_page(request: Request):
    miners_light = (await request.json())["miners"]
    if not miners_light:
        return RedirectResponse(request.url_for("manage_miners_page"), status_code=303)
    miners = await asyncio.gather(*[get_miner(miner) for miner in miners_light])
    await asyncio.gather(*[miner.reboot() for miner in miners])
    return RedirectResponse(request.url_for("manage_miners_page"), status_code=303)


@router.route("/restart_backend", methods=["POST"])
@login_req()
async def manage_miners_restart_backend_page(request: Request):
    miners_restart = (await request.json())["miners"]
    if not miners_restart:
        return RedirectResponse(request.url_for("manage_miners_page"), status_code=303)
    miners = await asyncio.gather(*[get_miner(miner) for miner in miners_restart])
    await asyncio.gather(*[miner.restart_backend() for miner in miners])
    return RedirectResponse(request.url_for("manage_miners_page"), status_code=303)


@router.route("/remove", methods=["POST"])
@login_req(["admin"])
async def manage_miners_remove_page(request: Request):
    miners_remove = (await request.json())["miners"]
    if not miners_remove:
        return RedirectResponse(request.url_for("manage_miners_page"), status_code=303)
    miners = await get_current_miner_list("*")
    for miner_ip in miners_remove:
        miners.remove(miner_ip)
    with open(settings.MINER_LIST, "w") as file:
        for miner_ip in miners:
            file.write(miner_ip + "\n")
    return RedirectResponse(request.url_for("manage_miners_page"), status_code=303)


@router.route("/remove_all")
@login_req(["admin"])
async def manage_miners_remove_all_page(request: Request):
    file = open(settings.MINER_LIST, "w")
    file.close()
    return RedirectResponse(request.url_for("dashboard_page"), status_code=303)
