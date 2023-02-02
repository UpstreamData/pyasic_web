from starlette.requests import Request

from pyasic_web.func import get_current_miner_list, get_user_ip_range, get_current_user
from pyasic_web.func.auth import login_req
from pyasic_web.templates import templates
from pyasic_web import settings


async def page_manage_miners(request: Request):
    await login_req(request, ["admin"])
    return templates.TemplateResponse(
        "manage_miners.html", {"request": request, "cur_miners": get_current_miner_list(await get_user_ip_range(request)), "user": await get_current_user(request)}
    )


async def page_remove_miners(request: Request):
    await login_req(request, ["admin"])
    miners_remove = (await request.json())["miners"]
    if not miners_remove:
        return await page_manage_miners(request)
    miners = get_current_miner_list("*")
    for miner_ip in miners_remove:
        miners.remove(miner_ip)
    with open(settings.MINER_LIST, "w") as file:
        for miner_ip in miners:
            file.write(miner_ip + "\n")
    return await page_manage_miners(request)
