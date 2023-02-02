from pyasic_web.auth import user_provider
from starlette.responses import RedirectResponse
from starlette.exceptions import HTTPException

async def login_req(request, _scopes: list = None):
    scopes = _scopes or []
    uid = request.session.get("_auth_user_id")
    if not uid:
        return RedirectResponse("/login")
    user = await user_provider.find_by_id(connection=request, identifier=uid)

    for scope in scopes:
        if scope not in user.get_scopes():
            raise HTTPException(403)
async def ws_login_req(ws, _scopes: list = None) -> None:
    scopes = _scopes or []
    uid = ws.session.get("_auth_user_id")
    if not uid:
        raise HTTPException(403)
    user = await user_provider.find_by_id(connection=ws, identifier=uid)

    for scope in scopes:
        if scope not in user.get_scopes():
            raise HTTPException(403)
