import ipaddress
import os

import aiofiles

from pyasic import MinerNetwork
from pyasic_web import settings
from pyasic_web.auth import user_provider


async def get_current_miner_list(allowed_ips: str = "*"):
    if not allowed_ips:
        return []
    cur_miners = []
    if os.path.exists(settings.MINER_LIST):
        async with aiofiles.open(settings.MINER_LIST) as file:
            async for line in file:
                cur_miners.append(line.strip())
    if not allowed_ips == "*":
        network = MinerNetwork(allowed_ips)
        cur_miners = [
            ip for ip in cur_miners if ipaddress.ip_address(ip) in network.hosts()
        ]
    cur_miners = sorted(cur_miners, key=lambda x: ipaddress.ip_address(x))
    return cur_miners


async def get_user_ip_range(request):
    uid = request.session.get("_auth_user_id")
    if uid:
        user = await user_provider.find_by_id(connection=request, identifier=uid)
        return user.ip_range
    else:
        return None


async def get_api_ip_range(api_key: str) -> str:
    user = await user_provider.find_by_api_key(api_key)
    if not user:
        return ""
    return user.ip_range


async def get_current_user(request):
    uid = request.session.get("_auth_user_id")
    if uid:
        user = await user_provider.find_by_id(connection=request, identifier=uid)
        return user
    else:
        return None


async def get_all_users():
    return user_provider.user_map


def get_available_cards(page):
    directory = os.path.join(settings.TEMPLATES_DIR, "cards", page)
    card_names = [
        str(f).replace(".html", "")
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]
    return sorted(card_names)
