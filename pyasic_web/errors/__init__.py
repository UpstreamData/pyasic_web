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

from pyasic_web.templates import templates


async def handle_400(request, exc):
    return templates.TemplateResponse(
        "error_pages/400.html",
        {"request": request, "title": exc.status_code},
        status_code=exc.status_code,
    )


async def handle_401(request, exc):
    return templates.TemplateResponse(
        "error_pages/401.html",
        {"request": request, "title": exc.status_code},
        status_code=exc.status_code,
    )


async def handle_403(request, exc):
    return templates.TemplateResponse(
        "error_pages/403.html",
        {"request": request, "title": exc.status_code},
        status_code=exc.status_code,
    )


async def handle_404(request, exc):
    return templates.TemplateResponse(
        "error_pages/404.html",
        {"request": request, "title": exc.status_code},
        status_code=exc.status_code,
    )


async def handle_429(request, exc):
    return templates.TemplateResponse(
        "error_pages/429.html",
        {"request": request, "title": exc.status_code},
        status_code=exc.status_code,
    )


async def handle_500(request, exc):
    if isinstance(exc, HTTPException):
        return templates.TemplateResponse(
            "error_pages/500.html",
            {"request": request, "title": exc.status_code},
            status_code=exc.status_code,
        )
    return templates.TemplateResponse(
        "error_pages/500.html", {"request": request, "title": 500}, status_code=500
    )


async def handle_502(request, exc):
    return templates.TemplateResponse(
        "error_pages/502.html",
        {"request": request, "title": exc.status_code},
        status_code=exc.status_code,
    )


async def handle_503(request, exc):
    return templates.TemplateResponse(
        "error_pages/503.html",
        {"request": request, "title": exc.status_code},
        status_code=exc.status_code,
    )


async def handle_504(request, exc):
    return templates.TemplateResponse(
        "error_pages/504.html",
        {"request": request, "title": exc.status_code},
        status_code=exc.status_code,
    )


exception_handlers = {
    400: handle_400,
    401: handle_401,
    403: handle_403,
    404: handle_404,
    429: handle_429,
    500: handle_500,
    502: handle_502,
    503: handle_503,
    504: handle_504,
}
