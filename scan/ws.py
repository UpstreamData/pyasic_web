import asyncio

from starlette.websockets import WebSocket, WebSocketDisconnect
from starlette.responses import RedirectResponse
import websockets.exceptions

from pyasic_web.scan.func import do_websocket_scan


async def scan_websocket(websocket):
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
