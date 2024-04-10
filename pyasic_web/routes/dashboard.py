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
from typing import Annotated

from fastapi import APIRouter, Depends, Security
from fastapi.requests import Request

from pyasic_web.auth import AUTH_SCHEME
from pyasic_web.api import v1
from pyasic_web.auth.users import get_current_user, User
from pyasic_web.func.miners import get_current_miner_list, load_balance
from pyasic_web.func.users import get_user_ip_range
from pyasic_web.templates import templates
from pyasic_web.templates.cards import (
    BasicCard,
    CountCard,
    GraphCard,
    PoolsCard,
    ErrorsCard,
    LightsCard,
    GRAPH_MODIFIER,
    AvailableCards,
)

router = APIRouter()


CARDS = AvailableCards(
    cards=[
        CountCard(
            title="Count",
            name="count",
            data_endpoint=v1.count.__name__,
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
            title="Expected Chips",
            name="expected_chips",
            data_endpoint=v1.expected_chips.__name__,
        ),
        GraphCard(
            title="Expected Chips",
            name="expected_chips",
            data_endpoint=v1.expected_chips.__name__,
        ),
        BasicCard(
            title="Expected Hashrate",
            name="expected_hashrate",
            data_endpoint=v1.expected_hashrate.__name__,
        ),
        GraphCard(
            title="Expected Hashrate",
            name="expected_hashrate",
            data_endpoint=v1.expected_hashrate.__name__,
        ),
        LightsCard(
            title="Lights",
            name="lights",
            data_endpoint=v1.lights.__name__,
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
        PoolsCard(
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
    ],
    modifiers=[GRAPH_MODIFIER],
)


@router.get("/dashboard")
async def dashboard_page(
    request: Request, current_user: Annotated[User, Depends(get_current_user)]
):
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "cur_miners": await get_current_miner_list(
                await get_user_ip_range(current_user)
            ),
            "user": current_user,
            "cards": CARDS,
            "data_endpoints": set(
                request.url_for(CARDS.get_card(c).data_endpoint).path
                for c in current_user.dashboard_cards
            ),
        },
    )


@router.post("/wattage", dependencies=[Security(AUTH_SCHEME, scopes=["admin"])])
async def dashboard_wattage_page(request: Request):
    d = await request.json()
    wattage = d["wattage"]
    if wattage:
        await load_balance(wattage)
