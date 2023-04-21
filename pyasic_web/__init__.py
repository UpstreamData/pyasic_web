from starlette.applications import Starlette
from fastapi import FastAPI
import asyncio
from pyasic_web.api.realtime import MinerDataManager

from pyasic_web import routes, auth, errors, api

tags_metadata = [
    {
        "name": "v1",
        "description": "API V1",
    }
]
app = FastAPI(
    title="pyasic Web API",
    version="1.0.0",
    contact={
        "name": "Upstream Data",
        "url": "https://github.com/UpstreamData/pyasic_web",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    middleware=[*auth.middleware],
    routes=routes.routes,
    exception_handlers=errors.exception_handlers,
    debug=True,
    openapi_tags=tags_metadata,
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)
app.include_router(api.router)


@app.on_event("startup")
async def app_startup():
    asyncio.create_task(MinerDataManager().run())
