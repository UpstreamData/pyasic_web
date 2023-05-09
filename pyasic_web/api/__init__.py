from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.requests import Request
from starlette.responses import JSONResponse

from pyasic_web import auth
from pyasic_web.func.web_settings import (  # noqa - Ignore access to _module
    get_current_settings,
)
from . import realtime
from . import v1
from pyasic_web.func.auth import login_req
from pyasic_web.func import get_current_user


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
    openapi_tags=tags_metadata,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    middleware=[*auth.middleware],
    root_path="/api"
)

@login_req()
async def docs(request: Request):
    return get_swagger_ui_html(openapi_url="/api/openapi.json", title="docs", swagger_ui_parameters={"api_key": (await get_current_user(request)).api_key})

@login_req()
async def get_openapi_schema(request: Request):
    return JSONResponse(get_openapi(title="FastAPI", version="1", routes=app.routes))


# router = APIRouter(prefix="/api")
app.include_router(v1.router)
app.include_router(realtime.router)
app.add_route("/openapi.json", get_openapi_schema, methods=["get"])
app.add_route("/", docs,  methods=["get"])
