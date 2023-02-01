import ipaddress
import os

from pyasic_web import settings


def get_current_miner_list():
    cur_miners = []
    if os.path.exists(settings.MINER_LIST):
        with open(settings.MINER_LIST) as file:
            for line in file.readlines():
                cur_miners.append(line.strip())
    cur_miners = sorted(cur_miners, key=lambda x: ipaddress.ip_address(x))
    return cur_miners
