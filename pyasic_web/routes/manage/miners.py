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
from typing import Annotated

import aiofiles
import websockets.exceptions
from fastapi import APIRouter, Security
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect

from pyasic import get_miner
from pyasic_web import settings
from pyasic_web.api.data import data_manager
from pyasic_web.auth import AUTH_SCHEME
from pyasic_web.auth.users import User, get_current_user
from pyasic_web.func.miners import (
    get_current_miner_list,
    update_miner_list,
    get_miner_phases,
    update_miner_phases,
)
from pyasic_web.func.users import get_user_ip_range

from pyasic_web.templates import templates

router = APIRouter()


@router.get("/")
async def manage_miners_page(
    request: Request, current_user: Annotated[User, Security(get_current_user)]
):
    return templates.TemplateResponse(
        "manage_miners.html",
        {
            "request": request,
            "cur_miners": await get_current_miner_list(
                await get_user_ip_range(current_user)
            ),
            "user": current_user,
        },
    )


@router.websocket("/ws")
async def manage_miners_ws(
    websocket: WebSocket, current_user: Annotated[User, Security(get_current_user)]
):
    await websocket.accept()
    miners = await get_current_miner_list(await get_user_ip_range(current_user))
    miner_phases = await get_miner_phases()
    miner_phases = {k: v for k, v in miner_phases.items() if k in miners}
    try:
        async for data in data_manager.subscribe():
            for miner in miners:
                if miner in data:
                    await websocket.send_json(
                        {
                            "ip": miner,
                            "model": data[miner].get("model", "Unknown"),
                            "hashrate": data[miner].get("hashrate", 0),
                            "percent_expected_chips": data[miner].get(
                                "percent_expected_chips", 0
                            ),
                            "errors": data[miner].get("errors", []),
                            "fault_light": data[miner].get("fault_light", False),
                            "phase": miner_phases[miner],
                        }
                    )
    except WebSocketDisconnect:
        print("Websocket disconnected.")
    except websockets.exceptions.ConnectionClosedOK:
        pass


@router.post("/light")
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


@router.post("/reboot")
async def manage_miners_reboot_page(request: Request):
    miners_light = (await request.json())["miners"]
    if not miners_light:
        return RedirectResponse(request.url_for("manage_miners_page"), status_code=303)
    miners = await asyncio.gather(*[get_miner(miner) for miner in miners_light])
    await asyncio.gather(*[miner.reboot() for miner in miners])
    return RedirectResponse(request.url_for("manage_miners_page"), status_code=303)


@router.post("/phase")
async def manage_miners_phase_page(request: Request):
    miners_phase = (await request.json())["miners"]
    phase_set = int((await request.json())["phase"])
    if not miners_phase:
        return RedirectResponse(request.url_for("manage_miners_page"), status_code=303)
    await update_miner_phases(miners_phase, phase_set)
    return RedirectResponse(request.url_for("manage_miners_page"), status_code=303)


@router.post("/restart_backend")
async def manage_miners_restart_backend_page(request: Request):
    miners_restart = (await request.json())["miners"]
    if not miners_restart:
        return RedirectResponse(request.url_for("manage_miners_page"), status_code=303)
    miners = await asyncio.gather(*[get_miner(miner) for miner in miners_restart])
    await asyncio.gather(*[miner.restart_backend() for miner in miners])
    return RedirectResponse(request.url_for("manage_miners_page"), status_code=303)


@router.post("/remove", dependencies=[Security(AUTH_SCHEME, scopes=["admin"])])
async def manage_miners_remove_page(request: Request):
    miners_remove = (await request.json())["miners"]
    if not miners_remove:
        return RedirectResponse(request.url_for("manage_miners_page"), status_code=303)
    miners = await get_current_miner_list("*")
    for miner_ip in miners_remove:
        miners.remove(miner_ip)
    await update_miner_list(miners)
    return RedirectResponse(request.url_for("manage_miners_page"), status_code=303)


@router.post("/remove_all", dependencies=[Security(AUTH_SCHEME, scopes=["admin"])])
async def manage_miners_remove_all_page(request: Request):
    await update_miner_list([])
    return RedirectResponse(request.url_for("dashboard_page"), status_code=303)
