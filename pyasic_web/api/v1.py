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

from typing import List

from fastapi import APIRouter

from .func import convert_hashrate, get_allowed_miners
from .realtime import MinerDataManager, get_data_by_selector
from .responses import MinerResponse, MinerSelector

router = APIRouter(prefix="/v1", tags=["v1"])


@router.post("/miners/")
async def miners(selector: MinerSelector) -> List[str]:
    return await get_allowed_miners(selector.api_key)


@router.post("/count/")
async def count(selector: MinerSelector) -> MinerResponse:
    return MinerResponse(value=len(await get_allowed_miners(selector.api_key)))


@router.post("/py_errors/")
async def py_errors(selector: MinerSelector) -> dict:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    miner_data = MinerDataManager().data
    data = {d: miner_data[d].get("py_error") for d in miner_data if d in allowed_miners}
    return {k: v for k, v in data.items() if v is not None}


@router.post("/api_ver/")
async def api_ver(selector: MinerSelector) -> dict:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    miner_data = MinerDataManager().data
    data = {d: miner_data[d].get("api_ver") for d in miner_data if d in allowed_miners}
    return {k: v for k, v in data.items() if v is not None}


@router.post("/efficiency/")
async def efficiency(selector: MinerSelector) -> MinerResponse:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    data = get_data_by_selector("efficiency", allowed_miners)

    if len(data) > 0:
        eff = sum(data) / len(data)
    else:
        eff = 0
    return MinerResponse(value=round(eff, 2), unit="J/TH")


@router.post("/env_temp/")
async def env_temp(selector: MinerSelector) -> MinerResponse:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    data = get_data_by_selector("env_temp", allowed_miners)

    data = list(filter(lambda x: x != -1, data))

    if len(data) > 0:
        temp = sum(data) / len(data)
    else:
        temp = 0
    return MinerResponse(value=round(temp, 2), unit="°C")


@router.post("/errors/")
async def errors(selector: MinerSelector) -> dict:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    miner_data = MinerDataManager().data
    data = {d: miner_data[d].get("errors") for d in miner_data if d in allowed_miners}

    data = {k: v for k, v in data.items() if v is not None}
    return data


@router.post("/fw_ver/")
async def fw_ver(selector: MinerSelector) -> dict:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    miner_data = MinerDataManager().data
    data = {d: miner_data[d].get("fw_ver") for d in miner_data if d in allowed_miners}
    return {k: v for k, v in data.items() if v is not None}


@router.post("/hashrate/")
async def hashrate(selector: MinerSelector) -> MinerResponse:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    data = get_data_by_selector("hashrate", allowed_miners)
    hr = sum(data)

    return MinerResponse(value=round(hr, 2), unit="TH/s")


@router.post("/hashrate_ths/")
async def hashrate(selector: MinerSelector) -> MinerResponse:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    data = get_data_by_selector("hashrate", allowed_miners)
    hr, unit = convert_hashrate(sum(data))

    return MinerResponse(value=round(hr, 2), unit=unit)


@router.post("/hostname/")
async def hostname(selector: MinerSelector) -> dict:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    miner_data = MinerDataManager().data
    data = {d: miner_data[d].get("hostname") for d in miner_data if d in allowed_miners}
    return {k: v for k, v in data.items() if v is not None}


@router.post("/ideal_chips/")
async def ideal_chips(selector: MinerSelector) -> MinerResponse:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    data = get_data_by_selector("ideal_chips", allowed_miners)

    return MinerResponse(
        value=sum(data),
    )


@router.post("/ideal_hashrate/")
async def ideal_hashrate(selector: MinerSelector) -> MinerResponse:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    data = get_data_by_selector("nominal_hashrate", allowed_miners)
    hr, unit = convert_hashrate(sum(data))

    return MinerResponse(value=round(hr, 2), unit=unit)


@router.post("/lights/")
async def lights(selector: MinerSelector) -> dict:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    miner_data = MinerDataManager().data
    data = {
        d: miner_data[d].get("fault_light") for d in miner_data if d in allowed_miners
    }

    data = {k: v for k, v in data.items() if v is not None}
    return data


@router.post("/make/")
async def make(selector: MinerSelector) -> dict:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    miner_data = MinerDataManager().data
    data = {d: miner_data[d].get("make") for d in miner_data if d in allowed_miners}
    return {k: v for k, v in data.items() if v is not None}


@router.post("/max_wattage/")
async def ideal_hashrate(selector: MinerSelector) -> MinerResponse:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    data = get_data_by_selector("wattage_limit", allowed_miners)

    return MinerResponse(value=sum(data), unit="W")


@router.post("/model/")
async def model(selector: MinerSelector) -> dict:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    miner_data = MinerDataManager().data
    data = {d: miner_data[d].get("model") for d in miner_data if d in allowed_miners}
    return {k: v for k, v in data.items() if v is not None}


@router.post("/pct_ideal_chips/")
async def pct_ideal_chips(selector: MinerSelector) -> MinerResponse:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    data = get_data_by_selector("percent_ideal_chips", allowed_miners)

    if len(data) > 0:
        ideal = sum(data) / len(data)
    else:
        ideal = 0

    return MinerResponse(value=round(ideal, 2), unit="%")


@router.post("/pct_ideal_hashrate/")
async def pct_ideal_hashrate(selector: MinerSelector) -> MinerResponse:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    data = get_data_by_selector("percent_ideal_hashrate", allowed_miners)

    if len(data) > 0:
        ideal = sum(data) / len(data)
    else:
        ideal = 0

    return MinerResponse(value=round(ideal, 2), unit="%")


@router.post("/pct_ideal_wattage/")
async def pct_ideal_wattage(selector: MinerSelector) -> MinerResponse:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    data = get_data_by_selector("percent_ideal_wattage", allowed_miners)

    if len(data) > 0:
        ideal = sum(data) / len(data)
    else:
        ideal = 0

    return MinerResponse(value=round(ideal, 2), unit="%")


@router.post("/pools/")
async def pools(selector: MinerSelector) -> dict:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    miner_data = MinerDataManager().data
    data = {
        d: miner_data[d].get("pool_1_user") for d in miner_data if d in allowed_miners
    }

    data = {k: v for k, v in data.items() if v is not None}
    return data


@router.post("/avg_temperature/")
async def avg_temperature(selector: MinerSelector) -> MinerResponse:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    data = get_data_by_selector("temperature_avg", allowed_miners)

    if len(data) > 0:
        ideal = sum(data) / len(data)
    else:
        ideal = 0

    return MinerResponse(value=round(ideal, 2), unit="°C")


@router.post("/total_chips/")
async def total_chips(selector: MinerSelector) -> MinerResponse:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    data = get_data_by_selector("total_chips", allowed_miners)

    return MinerResponse(value=sum(data))


@router.post("/total_wattage/")
async def total_wattage(selector: MinerSelector) -> MinerResponse:
    allowed_miners = await get_allowed_miners(selector.api_key, selector.miner_selector)
    data = get_data_by_selector("wattage", allowed_miners)

    return MinerResponse(value=sum(data), unit="W")
