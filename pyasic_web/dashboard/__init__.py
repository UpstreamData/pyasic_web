from fastapi import Request, APIRouter
from fastapi.responses import RedirectResponse

from pyasic_web.template import templates
from pyasic_web.func import get_current_miner_list

from .ws import router as ws_router

router = APIRouter()
router.include_router(ws_router)


@router.get("/")
def index(request: Request):
    return RedirectResponse(request.url_for("dashboard"))


@router.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "cur_miners": get_current_miner_list()}
    )
