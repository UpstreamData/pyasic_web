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
from __future__ import annotations
import ipaddress
import json
import os

import aiofiles

from pyasic import MinerNetwork
from pyasic_web import settings


async def get_current_miner_list(allowed_ips: str = "*"):
    if not allowed_ips:
        return []
    cur_miners = []
    if os.path.exists(settings.MINER_LIST):
        async with aiofiles.open(settings.MINER_LIST) as file:
            cur_miners = json.loads(await file.read())
    if not allowed_ips == "*":
        if isinstance(allowed_ips, str):
            allowed_ips = allowed_ips.replace(" ", "").split(",")
        network = MinerNetwork.from_list(allowed_ips)
        cur_miners = [
            ip for ip in cur_miners if ipaddress.ip_address(ip) in network.hosts
        ]
    cur_miners = sorted(cur_miners, key=lambda x: ipaddress.ip_address(x))
    return cur_miners


async def update_miner_list(miners: list[str]):
    async with aiofiles.open(settings.MINER_LIST, "w") as file:
        await file.write(json.dumps(miners))

    miner_phases = await get_miner_phases()
    new_miner_phases = {}
    for miner in miners:
        new_miner_phases[miner] = miner_phases.get(miner)

    async with aiofiles.open(settings.MINER_PHASE_LIST, "w") as file:
        await file.write(json.dumps(new_miner_phases))


async def get_miner_phases() -> dict:
    cur_miners = {}
    if os.path.exists(settings.MINER_PHASE_LIST):
        async with aiofiles.open(settings.MINER_PHASE_LIST) as file:
            cur_miners = json.loads(await file.read())
    return cur_miners
