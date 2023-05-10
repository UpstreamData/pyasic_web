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

from pyasic_web.auth import user_provider, AUTH_SCHEME, User
from pyasic_web.func import (
    get_all_users,
    get_current_miner_list,
    get_current_user,
    get_user_ip_range,
)
from pyasic_web.templates import templates

router = APIRouter(dependencies=[Security(AUTH_SCHEME, scopes=["admin"])])

@router.get("/")
async def manage_users_page(request: Request, current_user: Annotated[User, Security(get_current_user)]):
    return templates.TemplateResponse(
        "manage_users.html",
        {
            "request": request,
            "cur_miners": await get_current_miner_list(
                await get_user_ip_range(current_user)
            ),
            "user": current_user,
            "users": await get_all_users(),
        },
    )


@router.post("/delete")
async def manage_users_delete_page(request: Request):
    data = await request.json()
    uid = data["user_id"]
    user_provider.delete_user(uid)
    return RedirectResponse(request.url_for("manage_users_page"), status_code=303)


@router.post("/update")
async def manage_users_update_page(request: Request):
    data = await request.form()
    admin = data.get("admin")
    if admin:
        scope = ["admin"]
    else:
        scope = []
    user_provider.update_user(
        username=data["username"],
        name=data["name"],
        password=data["password"]
        if data["password"] and not data["password"] == ""
        else None,
        scopes=scope,
        ip_range=data["ip_range"],
    )
    return RedirectResponse(request.url_for("manage_users_page"), status_code=303)


@router.post("/add")
async def manage_users_add_page(request: Request):
    data = await request.form()
    admin = data.get("admin")
    if admin:
        scope = ["admin"]
    else:
        scope = []
    user_provider.add_user(
        username=data["username"],
        name=data["name"],
        password=data["password"]
        if data["password"] and not data["password"] == ""
        else None,
        scopes=scope,
        ip_range=data["ip_range"],
    )
    return RedirectResponse(request.url_for("manage_users_page"), status_code=303)
