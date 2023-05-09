from fastapi import APIRouter
from starlette.requests import Request

from pyasic_web.func import get_current_miner_list, get_current_user, get_user_ip_range
from pyasic_web.func.auth import login_req
from pyasic_web.func.web_settings import (  # noqa - Ignore access to _module
    get_current_settings,
)
from pyasic_web.templates import card_exists, templates

router = APIRouter(prefix="/dashboard")


@login_req()
@router.route("/")
async def page_dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "cur_miners": await get_current_miner_list(
                await get_user_ip_range(request)
            ),
            "user": await get_current_user(request),
            "card_exists": card_exists,
        },
    )
