import asyncio

from fastapi import APIRouter
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse

import pyasic
from pyasic_web import settings
from pyasic_web.func import get_current_miner_list, get_current_user, get_user_ip_range
from pyasic_web.func.auth import login_req
from pyasic_web.func.web_settings import (  # noqa - Ignore access to _module
    get_current_settings,
)
from pyasic_web.templates import card_exists, templates

router = APIRouter()


@login_req()
@router.route("/")
async def page_miner(request: Request):
    miner_ip = request.path_params["miner_ip"]
    miners = await get_current_miner_list(await get_user_ip_range(request))
    if miner_ip not in miners:
        raise HTTPException(403)

    return templates.TemplateResponse(
        "miner.html",
        {
            "request": request,
            "cur_miners": miners,
            "miner": miner_ip,
            "user": await get_current_user(request),
            "card_exists": card_exists,
        },
    )


@login_req()
@router.route("/remove")
async def page_remove_miner(request: Request):
    miner_ip = request.path_params["miner_ip"]
    miners = await get_current_miner_list("*")
    miners.remove(miner_ip)
    with open(settings.MINER_LIST, "w") as file:
        for miner_ip in miners:
            file.write(miner_ip + "\n")

    return RedirectResponse("/dashboard")


@login_req()
@router.route("/light")
async def page_light_miner(request: Request):
    miner_ip = request.path_params["miner_ip"]
    miner = await pyasic.get_miner(miner_ip)
    if miner.light:
        asyncio.create_task(miner.fault_light_off())
    else:
        asyncio.create_task(miner.fault_light_on())

    return RedirectResponse("/miner/" + miner_ip)


@login_req()
@router.route("/wattage")
async def page_wattage_set_miner(request: Request):
    miner_ip = request.path_params["miner_ip"]
    d = await request.json()
    wattage = d["wattage"]
    if wattage:
        miner = await pyasic.get_miner(miner_ip)
        await miner.set_power_limit(int(wattage))
