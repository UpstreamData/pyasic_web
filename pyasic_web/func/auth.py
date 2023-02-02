from pyasic_web.auth import user_provider
from starlette.responses import RedirectResponse
from starlette.exceptions import HTTPException

def login_req(_scopes: list = None):
    def decorator(func):
        async def inner(request):
            scopes = _scopes or []
            uid = request.session.get("_auth_user_id")
            if not uid:
                return RedirectResponse("/login")
            user = await user_provider.find_by_id(connection=request, identifier=uid)

            for scope in scopes:
                if scope not in user.get_scopes():
                    raise HTTPException(403)

            return await func(request)
        return inner
    return decorator
