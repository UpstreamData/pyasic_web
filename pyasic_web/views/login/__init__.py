from starlette.requests import Request
from starlette.responses import RedirectResponse

from pyasic_web.templates import templates
from pyasic_web.func import get_current_user
from pyasic_web.auth import login_manager, user_provider


async def page_login(request: Request):
    if request.method == "GET":
        if await get_current_user(request):
            return RedirectResponse("/dashboard", status_code=303)
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
            return RedirectResponse("/dashboard", status_code=303)
        else:
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "err": "Username or password is incorrect."},
            )

    return templates.TemplateResponse("login.html", {"request": request})


async def page_logout(request: Request):
    await login_manager.logout(request)
    return RedirectResponse(request.url_for("page_login"))
