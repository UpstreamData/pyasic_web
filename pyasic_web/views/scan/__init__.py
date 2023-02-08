import asyncio
import os

import websockets.exceptions
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.websockets import WebSocketDisconnect

from pyasic_web import settings
from pyasic_web.func import get_current_miner_list, get_user_ip_range, get_current_user
from pyasic_web.func.auth import login_req, ws_login_req
from pyasic_web.func.scan import do_websocket_scan
from pyasic_web.templates import templates


async def page_scan(request: Request):
    await login_req(request, ["admin"])
    return templates.TemplateResponse(
        "scan.html", {"request": request, "cur_miners": get_current_miner_list(await get_user_ip_range(request)), "user": await get_current_user(request)}
    )


async def page_add_miners_scan(request: Request):
    await login_req(request, ["admin"])
    miners = await request.json()
    with open(settings.MINER_LIST, "a+") as file:
        for miner_ip in miners["miners"]:
            file.write(miner_ip + "\n")
    return RedirectResponse("/scan")


async def ws_scan(websocket):
    await ws_login_req(websocket, ["admin"])
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
                cur_task = asyncio.create_task(do_websocket_scan(websocket, ws_data))
            if cur_task and cur_task.done():
                cur_task = None
    except WebSocketDisconnect:
        print("Websocket disconnected.")
    except websockets.exceptions.ConnectionClosedOK:
        pass
