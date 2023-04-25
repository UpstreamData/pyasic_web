from starlette.applications import Starlette
from fastapi import FastAPI
import asyncio
from pyasic_web.api.realtime import MinerDataManager

from pyasic_web import routes, auth, errors, api

app = Starlette(
    middleware=[*auth.middleware],
    routes=routes.routes,
    exception_handlers=errors.exception_handlers,
    debug=True
)
app.mount("/api", api.app)


@app.on_event("startup")
async def app_startup():
    asyncio.create_task(MinerDataManager().run())
