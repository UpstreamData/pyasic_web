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

from fastapi import APIRouter, Security
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

import pyasic
from pyasic_web import settings
from pyasic_web.auth import AUTH_SCHEME, User
from pyasic_web.func import get_current_miner_list, get_current_user, get_user_ip_range
from pyasic_web.func.web_settings import (  # noqa - Ignore access to _module
    get_current_settings,
)
from pyasic_web.templates import card_exists, templates

router = APIRouter()


@router.get("/")
async def miner_page(request: Request, current_user: Annotated[User, Security(get_current_user)]):
    miner_ip = request.path_params["miner_ip"]
    miners = await get_current_miner_list(await get_user_ip_range(current_user))
    if miner_ip not in miners:
        raise HTTPException(403)

    return templates.TemplateResponse(
        "miner.html",
        {
            "request": request,
            "cur_miners": miners,
            "miner": miner_ip,
            "user": current_user,
            "card_exists": card_exists,
        },
    )


@router.post("/remove", dependencies=[Security(AUTH_SCHEME, scopes=["admin"])])
async def miner_remove_page(request: Request):
    miner_ip = request.path_params["miner_ip"]
    miners = await get_current_miner_list("*")
    miners.remove(miner_ip)
    with open(settings.MINER_LIST, "w") as file:
        for miner_ip in miners:
            file.write(miner_ip + "\n")

    return RedirectResponse(request.url_for("dashboard_page"), status_code=303)


@router.post("/light", dependencies=[Security(AUTH_SCHEME, scopes=["admin"])])
async def miner_light_page(request: Request):
    miner_ip = request.path_params["miner_ip"]
    miner = await pyasic.get_miner(miner_ip)
    if miner.light:
        asyncio.create_task(miner.fault_light_off())
    else:
        asyncio.create_task(miner.fault_light_on())

    return RedirectResponse(request.url_for("miner_page", miner_ip=miner_ip), status_code=303)


@router.post("/wattage", dependencies=[Security(AUTH_SCHEME, scopes=["admin"])])
async def miner_wattage_page(request: Request):
    miner_ip = request.path_params["miner_ip"]
    d = await request.json()
    wattage = d["wattage"]
    if wattage:
        miner = await pyasic.get_miner(miner_ip)
        await miner.set_power_limit(int(wattage))
