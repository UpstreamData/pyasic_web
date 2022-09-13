from fastapi import Request, APIRouter
from fastapi.responses import RedirectResponse


from web_monitor.template import templates
from web_monitor.func import get_current_miner_list

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
