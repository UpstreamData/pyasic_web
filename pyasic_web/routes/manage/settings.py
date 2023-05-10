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
from typing import Annotated

from fastapi import APIRouter, Security
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from pyasic_web.func import get_current_miner_list, get_current_user, get_user_ip_range
from pyasic_web.func.web_settings import get_current_settings, update_settings
from pyasic_web.templates import templates
from pyasic_web.auth import AUTH_SCHEME, User

router = APIRouter(dependencies=[Security(AUTH_SCHEME, scopes=["admin"])])


@router.get("/")
async def manage_settings_page(request: Request, current_user: Annotated[User, Security(get_current_user)]):
    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "cur_miners": await get_current_miner_list(
                await get_user_ip_range(current_user)
            ),
            "settings": get_current_settings(),
            "user": current_user,
        },
    )


@router.post("/update")
async def manage_settings_update_page(request: Request):
    data = await request.form()
    data_sleep_time = data.get("data_sleep_time")
    miner_data_timeout = data.get("miner_data_timeout")
    miner_identify_timeout = data.get("miner_identify_timeout")
    new_settings = {
        "data_sleep_time": int(data_sleep_time),
        "miner_data_timeout": int(miner_data_timeout),
        "miner_identify_timeout": int(miner_identify_timeout),
    }
    update_settings(new_settings)
    return RedirectResponse(request.url_for("manage_settings_page"), status_code=303)
