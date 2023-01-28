from fastapi import Request, APIRouter
from fastapi.responses import RedirectResponse

import pyasic
import asyncio

from pyasic_web.template import templates
from pyasic_web.func import get_current_miner_list

from .ws import router as ws_router

router = APIRouter()
router.include_router(ws_router)


@router.get("/")
def miner(_request: Request, _miner_ip):
    return get_miner


@router.get("/{miner_ip}")
def get_miner(request: Request, miner_ip):
    return templates.TemplateResponse(
        "miner.html",
        {"request": request, "cur_miners": get_current_miner_list(), "miner": miner_ip},
    )


@router.get("/{miner_ip}/remove/")
def remove_miner(request: Request, miner_ip):
    miners = get_current_miner_list()
    miners.remove(miner_ip)
    with open("miner_list.txt", "w") as file:
        for miner_ip in miners:
            file.write(miner_ip + "\n")

    return RedirectResponse(request.url_for("dashboard"))


@router.get("/{miner_ip}/light/")
async def light_miner(request: Request, miner_ip):
    miner = await pyasic.get_miner(miner_ip)
    print(miner.light)
    if miner.light:
        asyncio.create_task(miner.fault_light_off())
    else:
        asyncio.create_task(miner.fault_light_on())

    return RedirectResponse(request.url_for("get_miner", miner_ip=miner_ip))


@router.post("/{miner_ip}/wattage/")
async def wattage_set_miner(request: Request, miner_ip):
    d = await request.json()
    wattage = d["wattage"]
    if wattage:
        miner = await pyasic.get_miner(miner_ip)
        await miner.set_power_limit(int(wattage))
