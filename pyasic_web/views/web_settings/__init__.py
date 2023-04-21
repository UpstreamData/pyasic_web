from starlette.requests import Request
from starlette.responses import RedirectResponse

from pyasic_web import settings
from pyasic_web.func import get_current_miner_list, get_user_ip_range, get_current_user
from pyasic_web.func.auth import login_req
from pyasic_web.func.web_settings import get_current_settings, update_settings
from pyasic_web.templates import templates


async def page_settings(request: Request):
    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "cur_miners": await get_current_miner_list(
                await get_user_ip_range(request)
            ),
            "settings": get_current_settings(),
            "user": await get_current_user(request),
        },
    )


async def page_update_settings(request: Request):
    data = await request.form()
    data_sleep_time = data.get("data_sleep_time")
    miner_data_timeout = data.get("miner_data_timeout")
    miner_identify_timeout = data.get("miner_identify_timeout")
    new_settings = {
        "data_sleep_time": int(data_sleep_time),
        "miner_data_timeout": int(miner_data_timeout),
        "miner_identify_timeout": int(miner_identify_timeout),
    }
    update_settings(new_settings)
    return RedirectResponse("/settings")


async def page_remove_all_miners(request: Request):
    file = open(settings.MINER_LIST, "w")
    file.close()
    return RedirectResponse("/dashboard")
