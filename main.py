import uvicorn
from starlette.applications import Starlette
from starlette.routing import Route, Mount, WebSocketRoute
from starlette.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from starlette.requests import Request

from pyasic_web._settings import settings, update_settings_page

from pyasic_web.dashboard import dashboard
from pyasic_web.dashboard.ws import dashboard_websocket

from pyasic_web.scan import add_miners_scan, scan
from pyasic_web.scan.ws import scan_websocket

from pyasic_web.miner import get_miner, remove_miner, wattage_set_miner, light_miner
from pyasic_web.miner.ws import miner_websocket
from pyasic_web.login import login_page


async def remove_all_miners(request: Request):
    file = open("miner_list.txt", "w")
    file.close()
    return RedirectResponse(request.url_for("dashboard"))


routes = [
    Route("/remove_all_miners", remove_all_miners),
    Mount("/static", app=StaticFiles(directory="static"), name="static"),
    Mount(
        "/scan",
        routes=[
            Route("/", scan),
            Route("/add_miners", add_miners_scan, methods=["POST"]),
            WebSocketRoute("/ws", scan_websocket),
        ],
    ),
    Mount(
        "/miner/{miner_ip}",
        routes=[
            Route("/", get_miner),
            Route("/remove", remove_miner),
            Route("/light", light_miner),
            Route("/wattage", wattage_set_miner),
            WebSocketRoute("/ws", miner_websocket),
        ],
    ),
    Mount(
        "/dashboard",
        routes=[Route("/", dashboard), WebSocketRoute("/ws", dashboard_websocket)],
    ),
    Mount(
        "/settings",
        routes=[Route("/", settings), Route("/update", update_settings_page, methods=["POST"])],
    ),
    Route("/login", login_page)
]

app = Starlette(debug=True, routes=routes)

def main():
    uvicorn.run("main:app", host="0.0.0.0", port=8080)

if __name__ == "__main__":
    main()
