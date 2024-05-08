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

import asyncio
import json
from typing import Annotated

import aiofiles
import pyasic
from fastapi import APIRouter, Security
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from pyasic_web import settings
from pyasic_web.api import v1
from pyasic_web.auth import AUTH_SCHEME
from pyasic_web.auth.users import get_current_user, User
from pyasic_web.func.miners import get_current_miner_list, update_miner_list
from pyasic_web.func.users import get_user_ip_range
from pyasic_web.templates import templates
from pyasic_web.templates.cards import (
    BasicCard,
    GraphCard,
    ErrorsCard,
    GRAPH_MODIFIER,
    AvailableCards,
    BooleanCard,
)

router = APIRouter()

CARDS = AvailableCards(
    cards=[
        BasicCard(
            title="API Version",
            name="api_ver",
            data_endpoint=v1.api_ver.__name__,
        ),
        BasicCard(
            title="Efficiency",
            name="efficiency",
            data_endpoint=v1.efficiency.__name__,
        ),
        GraphCard(
            title="Efficiency",
            name="efficiency",
            data_endpoint=v1.efficiency.__name__,
        ),
        BasicCard(
            title="Env Temperature",
            name="env_temp",
            data_endpoint=v1.env_temp.__name__,
        ),
        GraphCard(
            title="Env Temperature",
            name="env_temp",
            data_endpoint=v1.env_temp.__name__,
        ),
        ErrorsCard(
            title="Errors",
            name="errors",
            data_endpoint=v1.errors.__name__,
        ),
        BasicCard(
            title="FW Version",
            name="fw_ver",
            data_endpoint=v1.fw_ver.__name__,
        ),
        BasicCard(
            title="Hashrate",
            name="hashrate",
            data_endpoint=v1.hashrate.__name__,
        ),
        GraphCard(
            title="Hashrate",
            name="hashrate",
            data_endpoint=v1.hashrate.__name__,
        ),
        BasicCard(
            title="Hostname",
            name="hostname",
            data_endpoint=v1.hostname.__name__,
        ),
        BasicCard(
            title="Ideal Chips",
            name="expected_chips",
            data_endpoint=v1.expected_chips.__name__,
        ),
        GraphCard(
            title="Ideal Chips",
            name="expected_chips",
            data_endpoint=v1.expected_chips.__name__,
        ),
        BasicCard(
            title="Ideal Hashrate",
            name="expected_hashrate",
            data_endpoint=v1.expected_hashrate.__name__,
        ),
        GraphCard(
            title="Ideal Hashrate",
            name="expected_hashrate",
            data_endpoint=v1.expected_hashrate.__name__,
        ),
        BasicCard(
            title="Make",
            name="make",
            data_endpoint=v1.make.__name__,
        ),
        BasicCard(
            title="Max Wattage",
            name="max_wattage",
            data_endpoint=v1.max_wattage.__name__,
        ),
        GraphCard(
            title="Max Wattage",
            name="max_wattage",
            data_endpoint=v1.max_wattage.__name__,
        ),
        BasicCard(
            title="Model",
            name="model",
            data_endpoint=v1.model.__name__,
        ),
        BasicCard(
            title="% Ideal Chips",
            name="pct_expected_chips",
            data_endpoint=v1.pct_expected_chips.__name__,
        ),
        GraphCard(
            title="% Ideal Chips",
            name="pct_expected_chips",
            data_endpoint=v1.pct_expected_chips.__name__,
        ),
        BasicCard(
            title="% Ideal Hashrate",
            name="pct_expected_hashrate",
            data_endpoint=v1.pct_expected_hashrate.__name__,
        ),
        GraphCard(
            title="% Ideal Hashrate",
            name="pct_expected_hashrate",
            data_endpoint=v1.pct_expected_hashrate.__name__,
        ),
        BasicCard(
            title="% Ideal Wattage",
            name="pct_expected_wattage",
            data_endpoint=v1.pct_expected_wattage.__name__,
        ),
        GraphCard(
            title="% Ideal Wattage",
            name="pct_expected_wattage",
            data_endpoint=v1.pct_expected_wattage.__name__,
        ),
        BasicCard(
            title="Pools",
            name="pools",
            data_endpoint=v1.pools.__name__,
        ),
        BasicCard(
            title="Avg Temperature",
            name="temperature_avg",
            data_endpoint=v1.avg_temperature.__name__,
        ),
        GraphCard(
            title="Avg Temperature",
            name="temperature_avg",
            data_endpoint=v1.avg_temperature.__name__,
        ),
        BasicCard(
            title="Total Chips",
            name="total_chips",
            data_endpoint=v1.total_chips.__name__,
        ),
        GraphCard(
            title="Total Chips",
            name="total_chips",
            data_endpoint=v1.total_chips.__name__,
        ),
        BasicCard(
            title="Wattage",
            name="wattage",
            data_endpoint=v1.total_wattage.__name__,
        ),
        GraphCard(
            title="Wattage",
            name="wattage",
            data_endpoint=v1.total_wattage.__name__,
        ),
        BooleanCard(title="Nominal", name="nominal", data_endpoint=v1.nominal.__name__),
    ],
    modifiers=[GRAPH_MODIFIER],
)


@router.get("/")
async def miner_page(
    request: Request, current_user: Annotated[User, Security(get_current_user)]
):
    miner_ip = request.path_params["miner_ip"]
    miners = await get_current_miner_list(await get_user_ip_range(current_user))
    if miner_ip not in miners:
        raise HTTPException(403)

    return templates.TemplateResponse(
        "miner.html",
        {
            "request": request,
            "cur_miners": miners,
            "miner": miner_ip,
            "user": current_user,
            "cards": CARDS,
            "data_endpoints": set(
                request.url_for(CARDS.get_card(c).data_endpoint).path
                for c in current_user.miner_cards
            ),
        },
    )


@router.get("/remove", dependencies=[Security(AUTH_SCHEME, scopes=["admin"])])
async def miner_remove_page(request: Request):
    miner_ip = request.path_params["miner_ip"]
    miners = await get_current_miner_list("*")
    miners.remove(miner_ip)
    await update_miner_list(miners)
    return RedirectResponse(request.url_for("dashboard_page"), status_code=303)


@router.get("/light", dependencies=[Security(AUTH_SCHEME, scopes=["admin"])])
async def miner_light_page(request: Request):
    miner_ip = request.path_params["miner_ip"]
    miner = await pyasic.get_miner(miner_ip)
    if miner.light:
        await miner.fault_light_off()
    else:
        await miner.fault_light_on()

    return RedirectResponse(
        request.url_for("miner_page", miner_ip=miner_ip), status_code=303
    )


@router.post("/wattage", dependencies=[Security(AUTH_SCHEME, scopes=["admin"])])
async def miner_wattage_page(request: Request):
    miner_ip = request.path_params["miner_ip"]
    d = await request.json()
    wattage = d["wattage"]
    if wattage:
        miner = await pyasic.get_miner(miner_ip)
        await miner.set_power_limit(int(wattage))
