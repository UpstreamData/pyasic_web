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

from typing import Callable, Annotated

import websockets
import websockets.exceptions
from fastapi import APIRouter, WebSocket, Security, HTTPException
from fastapi.websockets import WebSocketDisconnect
from sse_starlette import EventSourceResponse
from starlette.requests import Request

from pyasic_web.api.responses import MinerSelector, MinerResponse, DataSelector
from pyasic_web.auth import AUTH_SCHEME
from pyasic_web.auth.users import get_current_user, User
from . import data

router = APIRouter(prefix="/realtime", dependencies=[Security(AUTH_SCHEME)])

MESSAGE_STREAM_RETRY_TIMEOUT = 15000  # MS



@router.websocket("/updates")
async def updates(websocket: WebSocket):
    await websocket.accept()
    async for update in data.data_manager.subscribe_to_updates():
        try:
            await websocket.send_json({"update": update})
        except WebSocketDisconnect:
            print("Websocket disconnected.")
            return
        except websockets.exceptions.ConnectionClosedError:
            print("Websocket disconnected.")
            return
        except websockets.exceptions.ConnectionClosedOK:
            return

@router.get("/updates")
async def updates():
    return EventSourceResponse(data.data_manager.subscribe_to_updates())
