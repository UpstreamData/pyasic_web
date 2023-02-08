from starlette.requests import Request
from starlette.responses import RedirectResponse

from pyasic_web.func import get_current_miner_list, get_user_ip_range, get_current_user, get_all_users
from pyasic_web.func.auth import login_req
from pyasic_web.templates import templates
from pyasic_web import settings
from pyasic_web.auth import user_provider


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
    return RedirectResponse(request.url_for("page_manage_users"), status_code=302)

async def page_manage_users(request: Request):
    await login_req(request, ["admin"])
    return templates.TemplateResponse(
        "manage_users.html", {"request": request, "cur_miners": get_current_miner_list(await get_user_ip_range(request)), "user": await get_current_user(request), "users": await get_all_users()}
    )

async def page_delete_user(request: Request):
    await login_req(request, ["admin"])
    data = await request.json()
    uid = data["user_id"]
    user_provider.delete_user(uid)
    return RedirectResponse(request.url_for("page_manage_users"), status_code=302)

async def page_update_user(request: Request):
    await login_req(request, ["admin"])
    data = await request.form()
    admin = data.get("admin")
    if admin:
        scope = ["admin"]
    else:
        scope = []
    user_provider.update_user(
        username=data["username"],
        name=data["name"],
        password=data["password"] if data["password"] and not data["password"] == "" else None,
        scopes=scope,
        ip_range=data["ip_range"],
    )
    return RedirectResponse(request.url_for("page_manage_users"), status_code=302)

async def page_add_user(request: Request):
    await login_req(request, ["admin"])
    data = await request.form()
    admin = data.get("admin")
    if admin:
        scope = ["admin"]
    else:
        scope = []
    user_provider.add_user(
        username=data["username"],
        name=data["name"],
        password=data["password"] if data["password"] and not data["password"] == "" else None,
        scopes=scope,
        ip_range=data["ip_range"],
    )
    return RedirectResponse(request.url_for("page_manage_users"), status_code=302)


async def page_manage_cards(request: Request):
    await login_req(request)
    return templates.TemplateResponse("manage_cards.html", {"request": request, "cur_miners": get_current_miner_list(await get_user_ip_range(request)), "user": await get_current_user(request)})

async def page_update_miner_cards(request: Request):
    await login_req(request)
    cards_raw = (await request.form())["miner_cards"]
    cards = cards_raw.split("&")
    for idx, card in enumerate(cards):
        card = card.replace("[]=card", "").replace("miner_", "")
        cards[idx] = card
    user = await get_current_user(request)
    user.miner_cards = cards
    user_provider.update_user_cards(user)
    return RedirectResponse(request.url_for("page_manage_cards"), status_code=302)

async def page_update_dashboard_cards(request: Request):
    await login_req(request)
    cards_raw = (await request.form())["dashboard_cards"]
    cards = cards_raw.split("&")
    for idx, card in enumerate(cards):
        card = card.replace("[]=card", "").replace("dashboard_", "")
        cards[idx] = card
    user = await get_current_user(request)
    user.dashboard_cards = cards
    user_provider.update_user_cards(user)
    return RedirectResponse(request.url_for("page_manage_cards"), status_code=302)
