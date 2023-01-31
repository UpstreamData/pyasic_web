from starlette.requests import Request

from pyasic_web.template import templates
from pyasic_web.func import get_current_miner_list

import os

dir_path = "\\".join(os.path.dirname(os.path.realpath(__file__)).split("\\")[:-1])


def scan(request: Request):
    print(request.url.port)
    return templates.TemplateResponse(
        "scan.html", {"request": request, "cur_miners": get_current_miner_list()}
    )


async def add_miners_scan(request: Request):
    miners = await request.json()
    with open(os.path.join(dir_path, "miner_list.txt"), "a+") as file:
        for miner_ip in miners["miners"]:
            file.write(miner_ip + "\n")
    return scan(request)
