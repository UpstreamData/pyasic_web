import asyncio
import json

from pyasic.miners.miner_factory import MinerFactory
from pyasic_web.errors.miner import MinerDataError
from pyasic_web.func.web_settings import (  # noqa - Ignore access to _module
    get_current_settings,
)


def get_pool_users_data(data: list):
    users = {}
    pool_data = [dp.get("pool_1_user") for dp in data]
    for user in pool_data:
        if user:
            if not user in users:
                users[user] = 0
            users[user] += 1
    return users


async def get_miner_data_dashboard(miner_ip):
    try:
        settings = get_current_settings()
        miner_identify_timeout = settings["miner_identify_timeout"]
        miner_data_timeout = settings["miner_data_timeout"]

        miner = await asyncio.wait_for(
            MinerFactory().get_miner(miner_ip), miner_identify_timeout
        )

        data = await asyncio.wait_for(miner.get_data(), miner_data_timeout)

        # return {"ip": str(miner_ip.ip), "hashrate": data.hashrate}
        return json.loads(data.as_json())

    except asyncio.exceptions.TimeoutError:
        return {"ip": miner_ip, "py_error": MinerDataError.NO_RESPONSE}

    except KeyError:
        return {
            "ip": miner_ip,
            "py_error": MinerDataError.BAD_DATA,
        }
