import ipaddress
import os

from pyasic_web import settings
from pyasic import MinerNetwork
from pyasic_web.auth import user_provider

def get_current_miner_list(allowed_ips: str = "*"):
    cur_miners = []
    if os.path.exists(settings.MINER_LIST):
        with open(settings.MINER_LIST) as file:
            for line in file.readlines():
                cur_miners.append(line.strip())
    if not allowed_ips == "*":
        network = MinerNetwork(allowed_ips)
        cur_miners = [ip for ip in cur_miners if ipaddress.ip_address(ip) in network.hosts()]
    cur_miners = sorted(cur_miners, key=lambda x: ipaddress.ip_address(x))
    return cur_miners

async def get_user_ip_range(request):
    uid = request.session.get("_auth_user_id")
    user = await user_provider.find_by_id(connection=request, identifier=uid)
    print(uid)
    return user.ip_range
