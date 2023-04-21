from starlette.requests import Request
from starlette.websockets import WebSocket, WebSocketDisconnect
from starlette.responses import RedirectResponse
import websockets.exceptions
import asyncio

from pyasic_web.func import (
    get_current_miner_list,
    get_user_ip_range,
    get_current_user,
    get_all_users,
    get_available_cards,
)
from pyasic_web.func.auth import login_req, ws_login_req
from pyasic_web.func.web_settings import get_current_settings
from pyasic_web.templates import templates
from pyasic_web import settings
from pyasic_web.auth import user_provider, DEFAULT_DASHBOARD_CARDS, DEFAULT_MINER_CARDS
from pyasic_web.api.realtime import MinerDataManager

from pyasic import get_miner


async def page_manage_miners(request: Request):
    await login_req(request)
    return templates.TemplateResponse(
        "manage_miners.html",
        {
            "request": request,
            "cur_miners": await get_current_miner_list(
                await get_user_ip_range(request)
            ),
            "user": await get_current_user(request),
        },
    )


async def ws_manage_miners(websocket: WebSocket):
    await ws_login_req(websocket)
    await websocket.accept()
    current_settings = get_current_settings()
    miner_data_timeout = current_settings["miner_data_timeout"]
    try:
        while True:
            try:
                miners = await get_current_miner_list(
                    await get_user_ip_range(websocket)
                )
                miners = await asyncio.gather(*[get_miner(miner) for miner in miners])
                data_tasks = asyncio.as_completed(
                    [
                        asyncio.wait_for(
                            miner.get_data(
                                data_to_get=[
                                    "hashrate",
                                    "model",
                                    "hashboards",
                                    "errors",
                                    "fault_light",
                                ]
                            ),
                            timeout=miner_data_timeout,
                        )
                        for miner in miners
                    ]
                )
                for task in data_tasks:
                    ret = await task
                    await websocket.send_text(ret.as_json())
                await asyncio.sleep(current_settings["graph_data_sleep_time"])
            except asyncio.exceptions.TimeoutError:
                pass
    except WebSocketDisconnect:
        print("Websocket disconnected.")
    except websockets.exceptions.ConnectionClosedOK:
        pass


async def page_light_miners(request: Request):
    await login_req(request)
    miners_light = (await request.json())["miners"]
    if not miners_light:
        return RedirectResponse(request.url_for("page_manage_miners"))
    miners = await asyncio.gather(*[get_miner(miner) for miner in miners_light])
    lights = await asyncio.gather(*[miner.check_light() for miner in miners])
    tasks = []
    for idx, miner in enumerate(miners):
        if lights[idx]:
            tasks.append(miner.fault_light_off())
        else:
            tasks.append(miner.fault_light_on())
    await asyncio.gather(*tasks)
    return RedirectResponse(request.url_for("page_manage_miners"))


async def page_reboot_miners(request: Request):
    await login_req(request)
    miners_light = (await request.json())["miners"]
    if not miners_light:
        return RedirectResponse(request.url_for("page_manage_miners"))
    miners = await asyncio.gather(*[get_miner(miner) for miner in miners_light])
    await asyncio.gather(*[miner.reboot() for miner in miners])
    return RedirectResponse(request.url_for("page_manage_miners"))


async def page_restart_backend_miners(request: Request):
    await login_req(request)
    miners_light = (await request.json())["miners"]
    if not miners_light:
        return RedirectResponse(request.url_for("page_manage_miners"))
    miners = await asyncio.gather(*[get_miner(miner) for miner in miners_light])
    await asyncio.gather(*[miner.restart_backend() for miner in miners])
    return RedirectResponse(request.url_for("page_manage_miners"))


async def page_remove_miners(request: Request):
    await login_req(request, ["admin"])
    miners_remove = (await request.json())["miners"]
    if not miners_remove:
        return RedirectResponse(request.url_for("page_manage_miners"))
    miners = await get_current_miner_list("*")
    for miner_ip in miners_remove:
        miners.remove(miner_ip)
    with open(settings.MINER_LIST, "w") as file:
        for miner_ip in miners:
            file.write(miner_ip + "\n")
    return RedirectResponse(request.url_for("page_manage_users"), status_code=302)


async def page_manage_users(request: Request):
    await login_req(request, ["admin"])
    return templates.TemplateResponse(
        "manage_users.html",
        {
            "request": request,
            "cur_miners": await get_current_miner_list(
                await get_user_ip_range(request)
            ),
            "user": await get_current_user(request),
            "users": await get_all_users(),
        },
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
        password=data["password"]
        if data["password"] and not data["password"] == ""
        else None,
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
        password=data["password"]
        if data["password"] and not data["password"] == ""
        else None,
        scopes=scope,
        ip_range=data["ip_range"],
    )
    return RedirectResponse(request.url_for("page_manage_users"), status_code=302)


async def page_manage_cards(request: Request):
    await login_req(request)
    return templates.TemplateResponse(
        "manage_cards.html",
        {
            "request": request,
            "cur_miners": await get_current_miner_list(
                await get_user_ip_range(request)
            ),
            "user": await get_current_user(request),
            "miner_available_cards": get_available_cards("miner"),
            "dashboard_available_cards": get_available_cards("dashboard"),
        },
    )


async def page_update_miner_cards(request: Request):
    await login_req(request)
    cards_raw = (await request.form())["miner_cards"]
    cards = cards_raw.split("&")
    if cards == [""]:
        cards = []
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
    if cards == [""]:
        cards = []
    for idx, card in enumerate(cards):
        card = card.replace("[]=card", "").replace("dashboard_", "")
        cards[idx] = card
    user = await get_current_user(request)
    user.dashboard_cards = cards
    user_provider.update_user_cards(user)
    return RedirectResponse(request.url_for("page_manage_cards"), status_code=302)


async def page_reset_cards(request: Request):
    await login_req(request)
    user = await get_current_user(request)
    user.miner_cards = DEFAULT_MINER_CARDS
    user.dashboard_cards = DEFAULT_DASHBOARD_CARDS
    user_provider.update_user_cards(user)
    return RedirectResponse(request.url_for("page_manage_cards"), status_code=302)
