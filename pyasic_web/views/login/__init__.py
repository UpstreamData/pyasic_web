from starlette.requests import Request
from starlette.responses import RedirectResponse

from pyasic_web.templates import templates
from pyasic_web.auth import login_manager


async def page_login(request: Request):
    if request.method == "GET":
        return templates.TemplateResponse("login.html", {"request": request})
    elif request.method == "POST":
        data = await request.form()
        user = data["username"]
        pwd = data["password"]
        if not user:
            return templates.TemplateResponse("login.html", {"request": request, "err": "Please enter a username."})
        if not pwd:
            return templates.TemplateResponse("login.html", {"request": request, "err": "Please enter a password."})
        token = await login_manager.login(request, user, pwd)
        if token:
            return RedirectResponse(request.url_for("page_dashboard"), status_code=303)
        else:
            return templates.TemplateResponse("login.html", {"request": request, "err": "Username or password is incorrect."})

    return templates.TemplateResponse("login.html", {"request": request})
