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
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from pyasic_web.auth import login_manager
from pyasic_web.func import get_current_user
from pyasic_web.templates import templates


async def login_page(request: Request):
    if request.method == "GET":
        if await get_current_user(request):
            return RedirectResponse(request.url_for("dashboard_page"), status_code=303)
        return templates.TemplateResponse("login.html", {"request": request})
    elif request.method == "POST":
        data = await request.form()
        user = data["username"]
        pwd = data["password"]
        if not user:
            return templates.TemplateResponse(
                "login.html", {"request": request, "err": "Please enter a username."}
            )
        if not pwd:
            return templates.TemplateResponse(
                "login.html", {"request": request, "err": "Please enter a password."}
            )
        token = await login_manager.login(request, user, pwd)
        if token:
            return RedirectResponse(request.url_for("dashboard_page"), status_code=303)
        else:
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "err": "Username or password is incorrect."},
            )

    return templates.TemplateResponse("login.html", {"request": request})


async def logout_page(request: Request):
    await login_manager.logout(request)
    return RedirectResponse(request.url_for("login_page"))
