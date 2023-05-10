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
from typing import Annotated

from fastapi import FastAPI, Security, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from pyasic_web.auth import User, user_provider
from pyasic_web.func.web_settings import (  # noqa - Ignore access to _module
    get_current_settings,
)
from . import realtime, v1
from .auth import get_current_user, Token, create_access_token

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
    root_path="/api",
)

@app.post("/login/", response_model=Token)
async def api_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await user_provider.verify(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(
        data={"sub": user.username, "scopes": [s for s in form_data.scopes if s in user.scopes]},
    )
    resp = JSONResponse({"access_token": access_token, "token_type": "bearer"})
    resp.set_cookie(
        "Authorization",
        value=f"Bearer {access_token}",
        max_age=1800,
        expires=1800,
    )
    return resp


async def docs(current_user: Annotated[User, Security(get_current_user)]):
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title="docs",
    )


async def get_openapi_schema(current_user: Annotated[User, Security(get_current_user)]):
    return JSONResponse(get_openapi(title="FastAPI", version="1", routes=app.routes))

@app.on_event("startup")
async def app_startup():
    asyncio.create_task(realtime.MinerDataManager().run())


app.include_router(v1.router)
app.include_router(realtime.router)
app.add_route("/openapi.json", get_openapi_schema, methods=["get"])
app.add_route("/", docs, methods=["get"])
