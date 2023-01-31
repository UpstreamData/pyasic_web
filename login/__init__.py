from fastapi import Request, APIRouter
from fastapi.responses import RedirectResponse

import pyasic
import asyncio

from pyasic_web.template import templates
from pyasic_web.func import get_current_miner_list

router = APIRouter()


@router.get("/")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
