from pydantic import BaseModel
from typing import List, Literal, Union

from fastapi import APIRouter


from pyasic_web.func import get_current_miner_list

router = APIRouter(prefix="/v1")

class MinerSelector(BaseModel):
    miners: Union[List, Literal["all"]]

class MinerResponse(BaseModel):
    value: Union[int, str, float]
    unit: str = ""

@router.get("/miners/")
async def miners() -> List[str]:
    return await get_current_miner_list()

@router.get("/count/")
async def count() -> MinerResponse:
    return MinerResponse(
        value=len(await get_current_miner_list())
    )

@router.post("/efficiency/")
async def efficiency() -> MinerResponse:
    return
