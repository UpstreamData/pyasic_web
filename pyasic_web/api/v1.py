from pydantic import BaseModel
from typing import List, Literal, Union, Tuple
from .realtime import MinerDataManager

from fastapi import APIRouter, HTTPException

from pyasic_web.func import get_current_miner_list, get_api_ip_range

router = APIRouter(prefix="/v1", tags=["v1"])


class MinerResponse(BaseModel):
    value: Union[float, int, str]
    unit: str = ""


class MinerSelector(BaseModel):
    api_key: str
    miner_selector: Union[List[str], str, Literal["all"]] = "all"


def convert_hashrate(ths_hr: float) -> Tuple[float, str]:
    hr = ths_hr
    if ths_hr == 0:
        hr_unit = "TH/s"
    elif ths_hr < 0.0001:
        hr_unit = "MH/s"
        hr = ths_hr * 1000000
    elif ths_hr < 1:
        hr_unit = "GH/s"
        hr = ths_hr * 1000
    elif ths_hr > 1000:
        hr_unit = "PH/s"
        hr = ths_hr / 1000
    else:
        hr_unit = "TH/s"
    return hr, hr_unit


def get_data_by_selector(
    data_key: str, selector: Union[List[str], str, Literal["all"]]
):
    miner_data = MinerDataManager().data
    if selector == "all":
        data = [miner_data[d].get(data_key) for d in miner_data]
    else:
        data = [miner_data[d].get(data_key) for d in miner_data if d in selector]
    return list(filter(lambda x: x is not None, data))


async def get_allowed_miners(
    api_key: str, selector: Union[List[str], str, Literal["all"]] = "all"
) -> list:
    allowed_range = await get_api_ip_range(api_key=api_key)
    if selector == "all":
        return await get_current_miner_list(allowed_range)
    if allowed_range == "*":
        return [ip for ip in await get_current_miner_list(selector)]
    return [ip for ip in await get_current_miner_list(selector) if ip in allowed_range]


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
    if selector.miner_selector == "all":
        data = {d: miner_data[d].get("errors") for d in miner_data}
    else:
        data = {
            d: miner_data[d].get("errors") for d in miner_data if d in allowed_miners
        }

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
