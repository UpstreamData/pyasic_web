# ------------------------------------------------------------------------------
#  Copyright 2022 Upstream Data Inc                                            -
#                                                                              -
#  Licensed under the Apache License, Version 2.0 (the "License");             -
#  you may not use this file except in compliance with the License.            -
#  You may obtain a copy of the License at                                     -
#                                                                              -
#      http://www.apache.org/licenses/LICENSE-2.0                              -
#                                                                              -
#  Unless required by applicable law or agreed to in writing, software         -
#  distributed under the License is distributed on an "AS IS" BASIS,           -
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.    -
#  See the License for the specific language governing permissions and         -
#  limitations under the License.                                              -
# ------------------------------------------------------------------------------

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from pyasic_web.auth import DEFAULT_DASHBOARD_CARDS, DEFAULT_MINER_CARDS, user_provider
from pyasic_web.func import (
    get_available_cards,
    get_current_miner_list,
    get_current_user,
    get_user_ip_range,
)
from pyasic_web.func.auth import login_req
from pyasic_web.templates import templates

router = APIRouter()

@router.route("/")
@login_req()
async def manage_cards_page(request: Request):
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

@router.route("/update_miner", methods=["POST"])
@login_req()
async def manage_cards_update_miner_page(request: Request):
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
    return RedirectResponse(request.url_for("manage_cards_page"), status_code=303)


@router.route("/update_dashboard", methods=["POST"])
@login_req()
async def manage_cards_update_dashboard_page(request: Request):
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
    return RedirectResponse(request.url_for("manage_cards_page"), status_code=303)


@router.route("/reset", methods=["POST"])
@login_req()
async def manage_cards_reset_page(request: Request):
    user = await get_current_user(request)
    user.miner_cards = DEFAULT_MINER_CARDS
    user.dashboard_cards = DEFAULT_DASHBOARD_CARDS
    user_provider.update_user_cards(user)
    return RedirectResponse(request.url_for("manage_cards_page"), status_code=303)
