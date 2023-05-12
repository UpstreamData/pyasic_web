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

from typing import Annotated, Dict

from fastapi import APIRouter, Security

from pyasic_web.auth.users import User, get_current_user
from .func import get_allowed_miners
from .realtime import create_return_by_selector
from .responses import *

router = APIRouter(prefix="/v1", tags=["v1"])


@router.post("/miners/")
@router.get("/miners/")
async def miners(current_user: Annotated[User, Security(get_current_user)]) -> List[str]:
    return await get_allowed_miners(current_user)


@router.post("/count/")
@router.get("/count/")
async def count(current_user: Annotated[User, Security(get_current_user)]) -> MinerIntegerResponse:
    return MinerIntegerResponse(value=len(await get_allowed_miners(current_user)))


@router.post("/py_errors/")
async def py_errors(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("py_error", allowed_miners, MinerErrorResponse)
    return MinerGroupResponse(data=data)


@router.post("/api_ver/")
async def api_ver(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("api_ver", allowed_miners, MinerStringResponse)
    return MinerGroupResponse(data=data)


@router.post("/efficiency/")
async def efficiency(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("efficiency", allowed_miners, MinerEfficiencyResponse)
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.AVG)


@router.post("/env_temp/")
async def env_temp(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("env_temp", allowed_miners, MinerTempResponse)
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.AVG)


@router.post("/errors/")
async def errors(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("errors", allowed_miners, MinerListResponse)
    return MinerGroupResponse(data=data)


@router.post("/fw_ver/")
async def fw_ver(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("fw_ver", allowed_miners, MinerStringResponse)
    return MinerGroupResponse(data=data)


@router.post("/hashrate_ths/")
async def hashrate_ths(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("hashrate", allowed_miners, MinerHashrateResponse)
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.SUM)


@router.post("/hashrate/")
async def hashrate(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("hashrate", allowed_miners, MinerHashrateResponse)
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.SUM)


@router.post("/hostname/")
async def hostname(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("hostname", allowed_miners, MinerStringResponse)
    return MinerGroupResponse(data=data)


@router.post("/ideal_chips/")
async def ideal_chips(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("ideal_chips", allowed_miners, MinerIntegerResponse)
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.SUM)


@router.post("/ideal_hashrate/")
async def ideal_hashrate(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("nominal_hashrate", allowed_miners, MinerHashrateResponse)
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.SUM)


@router.post("/lights/")
async def lights(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("fault_light", allowed_miners, MinerBooleanResponse)
    return MinerGroupResponse(data=data)


@router.post("/make/")
async def make(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("make", allowed_miners, MinerStringResponse)
    return MinerGroupResponse(data=data)


@router.post("/max_wattage/")
async def max_wattage(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("wattage_limit", allowed_miners, MinerWattageResponse)
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.SUM)


@router.post("/model/")
async def model(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("model", allowed_miners, MinerStringResponse)
    return MinerGroupResponse(data=data)


@router.post("/pct_ideal_chips/")
async def pct_ideal_chips(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("percent_ideal_chips", allowed_miners, MinerPercentageResponse)
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.AVG)


@router.post("/pct_ideal_hashrate/")
async def pct_ideal_hashrate(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("percent_ideal_hashrate", allowed_miners, MinerPercentageResponse)
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.AVG)


@router.post("/pct_ideal_wattage/")
async def pct_ideal_wattage(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("percent_ideal_wattage", allowed_miners, MinerWattageResponse)
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.AVG)


@router.post("/pools/")
async def pools(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("pool_1_user", allowed_miners, MinerStringResponse)
    return MinerGroupResponse(data=data)


@router.post("/avg_temperature/")
async def avg_temperature(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("temperature_avg", allowed_miners, MinerTempResponse)
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.AVG)


@router.post("/total_chips/")
async def total_chips(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("total_chips", allowed_miners, MinerIntegerResponse)
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.SUM)


@router.post("/total_wattage/")
async def total_wattage(selector: MinerSelector, current_user: Annotated[User, Security(get_current_user)]) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("wattage", allowed_miners, MinerWattageResponse)
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.SUM)
