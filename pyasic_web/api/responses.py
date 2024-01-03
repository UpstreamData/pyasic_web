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
from enum import Enum
from typing import List, Literal, Union, Dict, Optional

from pydantic import BaseModel

from pyasic_web.errors.miner import MinerDataError


class MinerSelector(BaseModel):
    miner_selector: Union[List[str], str, Literal["all"]] = "all"


class DataSelector(MinerSelector):
    data_selector: List[
        Literal[
            "api_ver",
            "efficiency",
            "env_temp",
            "errors",
            "fw_ver",
            "hashrate",
            "hostname",
            "expected_chips",
            "expected_hashrate",
            "lights",
            "make",
            "max_wattage",
            "model",
            "pct_expected_chips",
            "pct_expected_hashrate",
            "pct_expected_wattage",
            "pools",
            "avg_temperature",
            "total_chips",
            "total_wattage",
        ]
    ] = []


class MinerResponse(BaseModel):
    value: Union[float, int, str, list, bool, MinerDataError]
    unit: str = ""


class MinerStringResponse(MinerResponse):
    value: str


class MinerIntegerResponse(MinerResponse):
    value: int


class MinerFloatResponse(MinerResponse):
    value: float


class MinerListResponse(MinerResponse):
    value: list


class MinerBooleanResponse(MinerResponse):
    value: bool


class MinerErrorResponse(MinerResponse):
    value: MinerDataError


class MinerEfficiencyResponse(MinerResponse):
    value: float
    unit: str = "J/TH"


class MinerWattageResponse(MinerResponse):
    value: int
    unit: str = "W"


class MinerTempResponse(MinerResponse):
    value: float
    unit: str = "°C"


class MinerHashrateResponse(MinerResponse):
    value: float
    unit: Literal["MH/s", "GH/s", "TH/s", "PH/s"] = "TH/s"


class MinerPercentageResponse(MinerResponse):
    value: float
    unit: str = "%"


class MinerCombineMethod(Enum):
    NONE = "none"
    AVG = "avg"
    SUM = "sum"


class MinerGroupResponse(BaseModel):
    data: Optional[Dict[str, MinerResponse]]
    combine_method: MinerCombineMethod = MinerCombineMethod.NONE
