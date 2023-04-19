import asyncio
import ipaddress

from starlette.websockets import WebSocket

from pyasic.network import MinerNetwork
from pyasic_web.func import get_current_miner_list, get_user_ip_range


async def do_websocket_scan(websocket: WebSocket, network_ip: str):
    cur_miners = await get_current_miner_list(await get_user_ip_range(websocket))
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
