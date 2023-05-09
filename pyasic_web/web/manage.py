import asyncio

import websockets.exceptions
from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect

from pyasic import get_miner
from pyasic_web import settings
from pyasic_web.api.realtime import MinerDataManager
from pyasic_web.auth import DEFAULT_DASHBOARD_CARDS, DEFAULT_MINER_CARDS, user_provider
from pyasic_web.func import (
    get_all_users,
    get_available_cards,
    get_current_miner_list,
    get_current_user,
    get_user_ip_range,
)
from pyasic_web.func.auth import login_req
from pyasic_web.templates import templates

router = APIRouter(prefix="/manage")


@login_req()
@router.route("/miners")
async def page_manage_miners(request: Request):
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


@login_req()
@router.websocket("/manage_miners/ws")
async def ws_manage_miners(websocket: WebSocket):
    await websocket.accept()
    miners = await get_current_miner_list(await get_user_ip_range(websocket))
    try:
        async for data in MinerDataManager().subscribe():
            for miner in miners:
                if miner in data:
                    await websocket.send_text(data[miner].as_json())
    except WebSocketDisconnect:
        print("Websocket disconnected.")
    except websockets.exceptions.ConnectionClosedOK:
        pass


@login_req()
@router.route("/light_miners", methods=["POST"])
async def page_light_miners(request: Request):
    miners_light = (await request.json())["miners"]
    if not miners_light:
        return RedirectResponse(request.url_for("page_manage_miners"), status_code=303)
    miners = await asyncio.gather(*[get_miner(miner) for miner in miners_light])
    lights = await asyncio.gather(*[miner.check_light() for miner in miners])
    tasks = []
    for idx, miner in enumerate(miners):
        if lights[idx]:
            tasks.append(miner.fault_light_off())
        else:
            tasks.append(miner.fault_light_on())
    await asyncio.gather(*tasks)
    return RedirectResponse(request.url_for("page_manage_miners"), status_code=303)


@login_req()
@router.route("/reboot_miners", methods=["POST"])
async def page_reboot_miners(request: Request):
    miners_light = (await request.json())["miners"]
    if not miners_light:
        return RedirectResponse(request.url_for("page_manage_miners"), status_code=303)
    miners = await asyncio.gather(*[get_miner(miner) for miner in miners_light])
    await asyncio.gather(*[miner.reboot() for miner in miners])
    return RedirectResponse(request.url_for("page_manage_miners"), status_code=303)


@login_req()
@router.route("/restart_backend_miners", methods=["POST"])
async def page_restart_backend_miners(request: Request):
    miners_restart = (await request.json())["miners"]
    if not miners_restart:
        return RedirectResponse(request.url_for("page_manage_miners"), status_code=303)
    miners = await asyncio.gather(*[get_miner(miner) for miner in miners_restart])
    await asyncio.gather(*[miner.restart_backend() for miner in miners])
    return RedirectResponse(request.url_for("page_manage_miners"), status_code=303)


@login_req(["admin"])
@router.route("/remove_miners", methods=["POST"])
async def page_remove_miners(request: Request):
    miners_remove = (await request.json())["miners"]
    if not miners_remove:
        return RedirectResponse(request.url_for("page_manage_miners"), status_code=303)
    miners = await get_current_miner_list("*")
    for miner_ip in miners_remove:
        miners.remove(miner_ip)
    with open(settings.MINER_LIST, "w") as file:
        for miner_ip in miners:
            file.write(miner_ip + "\n")
    return RedirectResponse(request.url_for("page_manage_users"), status_code=303)


@login_req(["admin"])
@router.route("/users")
async def page_manage_users(request: Request):
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


@login_req(["admin"])
@router.route("/delete_user", methods=["POST"])
async def page_delete_user(request: Request):
    data = await request.json()
    uid = data["user_id"]
    user_provider.delete_user(uid)
    return RedirectResponse(request.url_for("page_manage_users"), status_code=303)


@login_req(["admin"])
@router.route("/update_user", methods=["POST"])
async def page_update_user(request: Request):
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
    return RedirectResponse(request.url_for("page_manage_users"), status_code=303)


@login_req(["admin"])
@router.route("/add_user", methods=["POST"])
async def page_add_user(request: Request):
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
    return RedirectResponse(request.url_for("page_manage_users"), status_code=303)


@login_req()
@router.route("/cards")
async def page_manage_cards(request: Request):
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


@login_req()
@router.route("/update_miner_cards", methods=["POST"])
async def page_update_miner_cards(request: Request):
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
    return RedirectResponse("/manage/cards", status_code=302)


@login_req()
@router.route("/update_dashboard_cards", methods=["POST"])
async def page_update_dashboard_cards(request: Request):
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
    return RedirectResponse("/manage/cards", status_code=303)


@login_req()
@router.route("/reset_cards", methods=["POST"])
async def page_reset_cards(request: Request):
    user = await get_current_user(request)
    user.miner_cards = DEFAULT_MINER_CARDS
    user.dashboard_cards = DEFAULT_DASHBOARD_CARDS
    user_provider.update_user_cards(user)
    return RedirectResponse(request.url_for("page_manage_cards"), status_code=303)
