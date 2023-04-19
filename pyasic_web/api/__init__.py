from fastapi import APIRouter

from . import v1
from . import realtime


router = APIRouter(prefix="/api")
router.include_router(v1.router)
router.include_router(realtime.router)
