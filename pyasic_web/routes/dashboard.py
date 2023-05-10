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

from fastapi import APIRouter, Security, Depends
from fastapi.requests import Request

from pyasic_web.auth import User
from pyasic_web.func import get_current_miner_list, get_current_user, get_user_ip_range
from pyasic_web.func.web_settings import (  # noqa - Ignore access to _module
    get_current_settings,
)
from pyasic_web.templates import card_exists, templates

router = APIRouter()

@router.get("/dashboard")
async def dashboard_page(request: Request, current_user: Annotated[User, Depends(get_current_user)]):
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "cur_miners": await get_current_miner_list(
                await get_user_ip_range(current_user)
            ),
            "user": current_user,
            "card_exists": card_exists,
        },
    )
