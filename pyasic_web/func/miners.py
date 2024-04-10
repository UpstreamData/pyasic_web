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

import asyncio
import ipaddress
import json
import os

import aiofiles
import pyasic

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


async def update_miner_phases(miners: list[str], phase: int):
    current_phases = await get_miner_phases()
    for miner in miners:
        try:
            current_phases[miner] = phase
        except KeyError:
            pass
    async with aiofiles.open(settings.MINER_PHASE_LIST, "w") as file:
        await file.write(json.dumps(current_phases))


async def load_balance(total_wattage: int):
    miners = await get_miner_phases()
    # for now, assume all miners support wattage tuning
    miners_by_phase = {1: [], 2: [], 3: [], None: []}
    for k, v in miners.items():
        miners_by_phase[v] = k

    phase_count = len([x for x in miners_by_phase if not len(miners_by_phase[x]) == 0])
    wattage_per_phase = total_wattage // phase_count
    for phase_miners in miners_by_phase.values():
        setpoints = await get_phase_setpoint(wattage_per_phase, phase_miners)
        await asyncio.gather(*[disable_miner(miner) for miner in setpoints["disable"]])
        await asyncio.gather(
            *[
                set_miner_wattage(miner, setpoints["wattage"])
                for miner in setpoints["tune"]
            ]
        )
    return True


async def disable_miner(ip: str):
    miner = await pyasic.get_miner(ip)
    await miner.stop_mining()


async def set_miner_wattage(ip: str, wattage: int):
    miner = await pyasic.get_miner(ip)
    await miner.resume_mining()
    await miner.set_power_limit(wattage)


async def get_phase_setpoint(
    phase_wattage: int, miners: list[str]
) -> dict[str, int | list[str]]:
    # assume all miners use 3600 at most
    MAX_WATTAGE = 3600
    MIN_WATTAGE = 1800
    DISABLED_USAGE = 50
    # do we need to turn miners off?
    disable_miners = len(miners) - phase_wattage // MIN_WATTAGE
    if disable_miners < 0:
        disable_miners = 0

    tune_miners = len(miners) - disable_miners
    wattage_per_miner = (
        phase_wattage - (DISABLED_USAGE * disable_miners)
    ) // tune_miners
    if wattage_per_miner > MAX_WATTAGE:
        wattage_per_miner = MAX_WATTAGE
    return {
        "wattage": wattage_per_miner,
        "disable": miners[:disable_miners],
        "tune": miners[disable_miners:],
    }
