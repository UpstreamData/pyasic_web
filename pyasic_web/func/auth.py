from starlette.exceptions import HTTPException
from starlette.responses import RedirectResponse

from pyasic_web.auth import user_provider


def login_req(_scopes: list = None):
    def decorator(func):
        # handle the inner function that the decorator is wrapping
        async def inner(*args, **kwargs):
            scopes = _scopes or []
            request = kwargs.get("request") or kwargs.get("websocket") or args[0]
            uid = request["session"].get("_auth_user_id")
            if not uid:
                return RedirectResponse(request.url_for("page_login"))
            user = await user_provider.find_by_id(connection=request, identifier=uid)
            for scope in scopes:
                if scope not in user.get_scopes():
                    raise HTTPException(403)

            return await func(*args, **kwargs)

        return inner

    return decorator
