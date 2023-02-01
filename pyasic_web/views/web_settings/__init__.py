from starlette.requests import Request
from starlette.responses import RedirectResponse

from pyasic_web import settings
from pyasic_web.func import get_current_miner_list
from pyasic_web.func.web_settings import get_current_settings, update_settings
from pyasic_web.templates import templates


async def page_settings(request: Request):
    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "cur_miners": get_current_miner_list(),
            "settings": get_current_settings(),
        },
    )


async def page_update_settings(request: Request):
    data = await request.form()
    graph_data_sleep_time = data.get("graph_data_sleep_time")
    miner_data_timeout = data.get("miner_data_timeout")
    miner_identify_timeout = data.get("miner_identify_timeout")
    new_settings = {
        "graph_data_sleep_time": int(graph_data_sleep_time),
        "miner_data_timeout": int(miner_data_timeout),
        "miner_identify_timeout": int(miner_identify_timeout),
    }
    update_settings(new_settings)
    return RedirectResponse(request.url_for("page_settings"))


async def page_remove_all_miners(request: Request):
    file = open(settings.MINER_LIST, "w")
    file.close()
    return RedirectResponse(request.url_for("page_dashboard"))
