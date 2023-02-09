from pyasic_web.templates import templates
from starlette.exceptions import HTTPException


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
