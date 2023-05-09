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

from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse

from pyasic_web.auth import user_provider
from functools import wraps

def login_req(_scopes: list = None):
    def decorator(func):
        # handle the inner function that the decorator is wrapping
        @wraps(func)
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
