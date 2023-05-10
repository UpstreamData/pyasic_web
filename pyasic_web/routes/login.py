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

from fastapi import APIRouter, HTTPException
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from pyasic_web.api import create_access_token
from pyasic_web.auth import user_provider, AUTH_SCHEME
from pyasic_web.templates import templates

router = APIRouter()

@router.get("/login")
@router.get("/")
async def login_page_get(request: Request):
    try:
        await AUTH_SCHEME(request)
    except HTTPException:
        return templates.TemplateResponse("login.html", {"request": request})
    else:
        return RedirectResponse(request.url_for("dashboard_page"), status_code=303)

@router.post("/login")
@router.post("/")
async def login_page(request: Request):
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
    if await user_provider.verify(user, pwd):
        current_user = await user_provider.find_by_username(user)
        access_token = create_access_token(
            data={"sub": current_user.username,
                  "scopes": current_user.scopes},
        )
        resp = RedirectResponse(request.url_for("dashboard_page"), status_code=303)
        resp.set_cookie(
            "Authorization",
            value=f"Bearer {access_token}",
            max_age=1800,
            expires=1800,
        )
        return resp
    else:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "err": "Username or password is incorrect."},
        )


@router.get("/logout")
@router.post("/logout")
async def logout_page(request: Request):
    resp = RedirectResponse(request.url_for("login_page"))
    resp.delete_cookie("Authorization")
    return resp
