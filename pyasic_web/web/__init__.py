from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from pyasic_web import auth, errors, settings
from . import dashboard, login, manage, miner, scan, web_settings

app = FastAPI(
    middleware=[*auth.middleware],
    exception_handlers=errors.exception_handlers,
    debug=True,
)

# add static directory
static = StaticFiles(directory=settings.STATIC_DIR)
app.mount("/static", app=static, name="static")

app.include_router(dashboard.router, prefix="/dashboard")
app.include_router(miner.router, prefix="/miner/{miner_ip}")

app.include_router(manage.router, prefix="/manage")
app.include_router(scan.router, prefix="/scan")
app.include_router(web_settings.router, prefix="/settings")

app.add_route("/", login.page_login, methods=["GET", "POST"])
app.add_route("/login", login.page_login, methods=["GET", "POST"])
app.add_route("/logout", login.page_logout)
app.add_route("/remove_all_miners", web_settings.page_remove_all_miners)
