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

from fastapi import APIRouter, Security

from pyasic_web.auth.users import User, get_current_user
from . import data
from .func import get_allowed_miners
from .responses import *
from ..func.miners import load_balance

router = APIRouter(prefix="/v1", tags=["v1"])


@router.post("/miners/")
@router.get("/miners/")
async def miners(
    current_user: Annotated[User, Security(get_current_user)]
) -> List[str]:
    return await data.miners(current_user)


@router.post("/count/")
@router.get("/count/")
async def count(
    current_user: Annotated[User, Security(get_current_user)]
) -> MinerIntegerResponse:
    return await data.count(current_user)


@router.post("/py_errors/")
async def py_errors(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.py_errors(selector, current_user)


@router.post("/api_ver/")
async def api_ver(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.api_ver(selector, current_user)


@router.post("/efficiency/")
async def efficiency(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.efficiency(selector, current_user)


@router.post("/env_temp/")
async def env_temp(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.env_temp(selector, current_user)


@router.post("/errors/")
async def errors(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.errors(selector, current_user)


@router.post("/fw_ver/")
async def fw_ver(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.fw_ver(selector, current_user)


@router.post("/hashrate_ths/")
async def hashrate_ths(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.hashrate_ths(selector, current_user)


@router.post("/hashrate/")
async def hashrate(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.hashrate(selector, current_user)


@router.post("/hostname/")
async def hostname(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.hostname(selector, current_user)


@router.post("/expected_chips/")
async def expected_chips(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.expected_chips(selector, current_user)


@router.post("/expected_hashrate/")
async def expected_hashrate(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.expected_hashrate(selector, current_user)


@router.post("/lights/")
async def lights(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.lights(selector, current_user)


@router.post("/make/")
async def make(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.make(selector, current_user)


@router.post("/max_wattage/")
async def max_wattage(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.max_wattage(selector, current_user)


@router.post("/model/")
async def model(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.model(selector, current_user)


@router.post("/pct_expected_chips/")
async def pct_expected_chips(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.pct_expected_chips(selector, current_user)


@router.post("/pct_expected_hashrate/")
async def pct_expected_hashrate(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.pct_expected_hashrate(selector, current_user)


@router.post("/pct_expected_wattage/")
async def pct_expected_wattage(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.pct_expected_wattage(selector, current_user)


@router.post("/pools/")
async def pools(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.pools(selector, current_user)


@router.post("/avg_temperature/")
async def avg_temperature(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.avg_temperature(selector, current_user)


@router.post("/total_chips/")
async def total_chips(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.total_chips(selector, current_user)


@router.post("/total_wattage/")
async def total_wattage(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.total_wattage(selector, current_user)


@router.post("/nominal/")
async def nominal(
    selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]
) -> MinerGroupResponse:
    return await data.nominal(selector, current_user)


@router.post("/set_wattage/")
async def nominal(
    selector: MinerSelector,
    current_user: Annotated[User, Security(get_current_user)],
    wattage: int,
) -> bool:
    return await load_balance(wattage)
