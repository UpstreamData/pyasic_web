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
from typing import List, Literal, Union, Dict

import pyasic
from pyasic_web.api.func import get_allowed_miners
from pyasic_web.api.responses import (
    MinerSelector,
    MinerGroupResponse,
    MinerStringResponse,
    MinerErrorResponse,
    MinerIntegerResponse,
    MinerTempResponse,
    MinerEfficiencyResponse,
    MinerCombineMethod,
    MinerListResponse,
    MinerHashrateResponse,
    MinerBooleanResponse,
    MinerWattageResponse,
    MinerPercentageResponse,
    MinerResponse,
)
from pyasic_web.auth.users import User
from pyasic_web.errors.miner import MinerDataError
from pyasic_web.func.miners import get_current_miner_list
from pyasic_web.func.web_settings import get_current_settings


class MinerDataManager:
    def __init__(self):
        self.data = {}
        self.miners = []
        self._publish = asyncio.Event()

    async def run(self):
        graph_sleep_time = get_current_settings()["data_sleep_time"]
        while True:
            self.miners = await get_current_miner_list()
            d = await asyncio.gather(*[get_miner_data(m) for m in self.miners])
            self.data = {str(i["ip"]): i for i in d}
            await self.publish()
            await asyncio.sleep(graph_sleep_time)

    async def publish(self):
        self._publish.set()
        await asyncio.sleep(0)  # yield to event loop
        self._publish.clear()

    async def subscribe(self):
        if not self.data == {}:
            yield self.data
        while True:
            await self._publish.wait()
            yield self.data
            await asyncio.sleep(0)  # yield to event loop

    async def subscribe_to_updates(self):
        if not self.data == {}:
            yield True
        while True:
            await self._publish.wait()
            yield True
            await asyncio.sleep(0)  # yield to event loop


data_manager = MinerDataManager()


def get_data_by_selector(
    data_key: str, selector: Union[List[str], str, Literal["all"]]
) -> dict:
    miner_data = data_manager.data
    if selector == "all":
        data = {
            d: miner_data[d][data_key]
            for d in miner_data
            if miner_data[d].get(data_key) is not None
        }
    else:
        data = {
            d: miner_data[d][data_key]
            for d in miner_data
            if miner_data[d].get(data_key) is not None and d in selector
        }
    return data


async def get_miner_data(miner_ip: str):
    try:
        settings = get_current_settings()
        miner_identify_timeout = settings["miner_identify_timeout"]
        miner_data_timeout = settings["miner_data_timeout"]

        miner = await asyncio.wait_for(
            pyasic.get_miner(miner_ip), miner_identify_timeout
        )

        data = await asyncio.wait_for(miner.get_data(), miner_data_timeout)

        # return {"ip": str(miner_ip.ip), "hashrate": data.hashrate}
        return json.loads(data.as_json())

    except asyncio.exceptions.TimeoutError:
        return {"ip": miner_ip, "py_error": MinerDataError.NO_RESPONSE.value}

    except KeyError:
        return {
            "ip": miner_ip,
            "py_error": MinerDataError.BAD_DATA.value,
        }


def create_return_by_selector(
    data_key: str,
    selector: Union[List[str], str, Literal["all"]],
    ret_type: type(MinerResponse),
) -> Dict[str, type(MinerResponse)]:
    miner_data = data_manager.data
    if selector == "all":
        d = {
            d: ret_type(value=miner_data[d][data_key])
            for d in miner_data
            if miner_data[d].get(data_key) is not None
        }
    else:
        d = {
            d: ret_type(value=miner_data[d][data_key])
            for d in miner_data
            if miner_data[d].get(data_key) is not None and d in selector
        }
    return d


async def miners(current_user: User) -> List[str]:
    return await get_allowed_miners(current_user)


async def count(current_user: User) -> MinerIntegerResponse:
    return MinerIntegerResponse(value=len(await get_allowed_miners(current_user)))


async def py_errors(selector: MinerSelector, current_user: User) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("py_error", allowed_miners, MinerErrorResponse)
    return MinerGroupResponse(data=data)


async def api_ver(selector: MinerSelector, current_user: User) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("api_ver", allowed_miners, MinerStringResponse)
    return MinerGroupResponse(data=data)


async def efficiency(selector: MinerSelector, current_user: User) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector(
        "efficiency", allowed_miners, MinerEfficiencyResponse
    )
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.AVG)


async def env_temp(selector: MinerSelector, current_user: User) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("env_temp", allowed_miners, MinerTempResponse)
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.AVG)


async def errors(selector: MinerSelector, current_user: User) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("errors", allowed_miners, MinerListResponse)
    return MinerGroupResponse(data=data)


async def fw_ver(selector: MinerSelector, current_user: User) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("fw_ver", allowed_miners, MinerStringResponse)
    return MinerGroupResponse(data=data)


async def hashrate_ths(
    selector: MinerSelector, current_user: User
) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("hashrate", allowed_miners, MinerHashrateResponse)
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.SUM)


async def hashrate(selector: MinerSelector, current_user: User) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("hashrate", allowed_miners, MinerHashrateResponse)
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.SUM)


async def hostname(selector: MinerSelector, current_user: User) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("hostname", allowed_miners, MinerStringResponse)
    return MinerGroupResponse(data=data)


async def expected_chips(
    selector: MinerSelector, current_user: User
) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector(
        "expected_chips", allowed_miners, MinerIntegerResponse
    )
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.SUM)


async def expected_hashrate(
    selector: MinerSelector, current_user: User
) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector(
        "expected_hashrate", allowed_miners, MinerHashrateResponse
    )
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.SUM)


async def lights(selector: MinerSelector, current_user: User) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector(
        "fault_light", allowed_miners, MinerBooleanResponse
    )
    return MinerGroupResponse(data=data)


async def make(selector: MinerSelector, current_user: User) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("make", allowed_miners, MinerStringResponse)
    return MinerGroupResponse(data=data)


async def max_wattage(
    selector: MinerSelector, current_user: User
) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector(
        "wattage_limit", allowed_miners, MinerWattageResponse
    )
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.SUM)


async def model(selector: MinerSelector, current_user: User) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("model", allowed_miners, MinerStringResponse)
    return MinerGroupResponse(data=data)


async def pct_expected_chips(
    selector: MinerSelector, current_user: User
) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector(
        "percent_expected_chips", allowed_miners, MinerPercentageResponse
    )
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.AVG)


async def pct_expected_hashrate(
    selector: MinerSelector, current_user: User
) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector(
        "percent_expected_hashrate", allowed_miners, MinerPercentageResponse
    )
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.AVG)


async def pct_expected_wattage(
    selector: MinerSelector, current_user: User
) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector(
        "percent_expected_wattage", allowed_miners, MinerPercentageResponse
    )
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.AVG)


async def pools(selector: MinerSelector, current_user: User) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("pool_1_user", allowed_miners, MinerStringResponse)
    return MinerGroupResponse(data=data)


async def avg_temperature(
    selector: MinerSelector, current_user: User
) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector(
        "temperature_avg", allowed_miners, MinerTempResponse
    )
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.AVG)


async def total_chips(
    selector: MinerSelector, current_user: User
) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector(
        "total_chips", allowed_miners, MinerIntegerResponse
    )
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.SUM)


async def total_wattage(
    selector: MinerSelector, current_user: User
) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("wattage", allowed_miners, MinerWattageResponse)
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.SUM)


async def nominal(selector: MinerSelector, current_user: User) -> MinerGroupResponse:
    allowed_miners = await get_allowed_miners(current_user, selector.miner_selector)
    data = create_return_by_selector("nominal", allowed_miners, MinerBooleanResponse)
    return MinerGroupResponse(data=data, combine_method=MinerCombineMethod.NONE)
