from starlette.requests import Request

from pyasic_web.template import templates
from pyasic_web.func import get_current_miner_list


def dashboard(request: Request):
    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "cur_miners": get_current_miner_list()}
    )
