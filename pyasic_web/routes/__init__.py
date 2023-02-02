from starlette.routing import Mount, Route, WebSocketRoute, RedirectResponse
from starlette.staticfiles import StaticFiles

from pyasic_web import settings, views

static = StaticFiles(directory=settings.STATIC_DIR)

routes = [
    Route("/", views.login.page_login,  methods=["GET", "POST"]),
    Route("/remove_all_miners", views.web_settings.page_remove_all_miners),
    Mount("/static", app=static, name="static"),
    Mount(
        "/scan",
        routes=[
            Route("/", views.scan.page_scan),
            Route("/add_miners", views.scan.page_add_miners_scan, methods=["POST"]),
            WebSocketRoute("/ws", views.scan.ws_scan),
        ],
    ),
    Mount(
        "/miner/{miner_ip}",
        routes=[
            Route("/", views.miner.page_miner),
            Route("/remove", views.miner.page_remove_miner),
            Route("/light", views.miner.page_light_miner),
            Route("/wattage", views.miner.page_wattage_set_miner),
            WebSocketRoute("/ws", views.miner.ws_miner),
        ],
    ),
    Mount(
        "/dashboard",
        routes=[
            Route("/", views.dashboard.page_dashboard),
            WebSocketRoute("/ws", views.dashboard.ws_dashboard),
        ],
    ),
    Mount(
        "/settings",
        routes=[
            Route("/", views.web_settings.page_settings),
            Route("/update", views.web_settings.page_update_settings, methods=["POST"]),
        ],
    ),
    Route("/login", views.login.page_login, methods=["GET", "POST"]),
    Route("/logout", views.login.page_logout, methods=["GET"]),
]
