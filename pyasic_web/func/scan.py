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
import ipaddress

from fastapi.websockets import WebSocket

from pyasic.network import MinerNetwork
from pyasic_web.auth import AUTH_SCHEME, User
from pyasic_web.func import get_current_miner_list, get_user_ip_range


async def do_websocket_scan(websocket: WebSocket, user: User, network_ip: str):
    cur_miners = await get_current_miner_list(await get_user_ip_range(user))
    try:
        if "/" in network_ip:
            network_ip, network_subnet = network_ip.split("/")
            network = MinerNetwork(network_ip, mask=network_subnet)
        else:
            network = MinerNetwork(network_ip)
        miner_generator = network.scan_network_generator()
        all_miners = []
        async for found_miner in miner_generator:
            if found_miner and str(found_miner.ip) not in cur_miners:
                all_miners.append(
                    {"ip": str(found_miner.ip), "model": await found_miner.get_model()}
                )
                all_miners.sort(key=lambda x: ipaddress.ip_address(x["ip"]))
                await websocket.send_json(all_miners)
        await websocket.send_text("Done")
    except asyncio.CancelledError:
        raise
