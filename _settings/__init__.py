from starlette.requests import Request
from starlette.responses import RedirectResponse

from pyasic_web.template import templates
from pyasic_web.func import get_current_miner_list
from pyasic_web._settings.func import get_current_settings, update_settings


async def settings(request: Request):
    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "cur_miners": get_current_miner_list(),
            "settings": get_current_settings(),
        },
    )


async def update_settings_page(request: Request):
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
    return RedirectResponse(request.url_for("settings"))
