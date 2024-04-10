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
from fastapi.websockets import WebSocketDisconnect, WebSocket

from pyasic_web import settings
from pyasic_web.auth import AUTH_SCHEME
from pyasic_web.auth.users import User, get_current_user
from pyasic_web.func.miners import get_current_miner_list, update_miner_list

from pyasic_web.func.scan import do_websocket_scan
from pyasic_web.func.users import get_user_ip_range
from pyasic_web.templates import templates

router = APIRouter(dependencies=[Security(AUTH_SCHEME, scopes=["admin"])])


@router.get("/")
async def miner_scan_page(
    request: Request, current_user: Annotated[User, Security(get_current_user)]
):
    return templates.TemplateResponse(
        "scan.html",
        {
            "request": request,
            "cur_miners": await get_current_miner_list(
                await get_user_ip_range(current_user)
            ),
            "user": current_user,
        },
    )


@router.post("/add")
async def miner_scan_add_page(request: Request):
    miners = await request.json()
    await update_miner_list(miners["miners"])
    return RedirectResponse(request.url_for("dashboard_page"), status_code=303)


@router.websocket("/ws")
async def miner_scan_ws(
    websocket: WebSocket, current_user: Annotated[User, Security(get_current_user)]
):
    await websocket.accept()
    cur_task = None
    try:
        while True:
            ws_data = await websocket.receive_text()
            if "-Cancel-" in ws_data:
                if cur_task:
                    cur_task.cancel()
                    print("Cancelling scan...")
                    try:
                        await cur_task
                    except asyncio.CancelledError:
                        cur_task = None
                await websocket.send_text("Cancelled")
            else:
                cur_task = asyncio.create_task(
                    do_websocket_scan(websocket, current_user, ws_data)
                )
            if cur_task and cur_task.done():
                cur_task = None
    except WebSocketDisconnect:
        print("Websocket disconnected.")
    except websockets.exceptions.ConnectionClosedOK:
        pass
