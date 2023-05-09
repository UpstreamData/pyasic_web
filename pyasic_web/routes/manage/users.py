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

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from pyasic_web.auth import user_provider
from pyasic_web.func import (
    get_all_users,
    get_current_miner_list,
    get_current_user,
    get_user_ip_range,
)
from pyasic_web.func.auth import login_req
from pyasic_web.templates import templates

router = APIRouter()

@router.route("/")
@login_req(["admin"])
async def manage_users_page(request: Request):
    return templates.TemplateResponse(
        "manage_users.html",
        {
            "request": request,
            "cur_miners": await get_current_miner_list(
                await get_user_ip_range(request)
            ),
            "user": await get_current_user(request),
            "users": await get_all_users(),
        },
    )


@router.route("/delete", methods=["POST"])
@login_req(["admin"])
async def manage_users_delete_page(request: Request):
    data = await request.json()
    uid = data["user_id"]
    user_provider.delete_user(uid)
    return RedirectResponse(request.url_for("manage_users_page"), status_code=303)


@router.route("/update", methods=["POST"])
@login_req(["admin"])
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


@router.route("/add", methods=["POST"])
@login_req(["admin"])
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
