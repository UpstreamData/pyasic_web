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
from typing import List, Literal, Tuple, Union

from pyasic_web.auth import User
from pyasic_web.func import get_user_ip_range, get_current_miner_list


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


async def get_allowed_miners(
    user: User, selector: Union[List[str], str, Literal["all"]] = "all"
) -> list:
    allowed_range = await get_user_ip_range(user)
    if selector == "all":
        return await get_current_miner_list(allowed_range)
    if allowed_range == "*":
        return [ip for ip in await get_current_miner_list(selector)]
    return [ip for ip in await get_current_miner_list(selector) if ip in allowed_range]
