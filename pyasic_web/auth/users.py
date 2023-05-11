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

import json
import os
from copy import copy
from typing import Annotated
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import (
    SecurityScopes,
)
from jose import jwt, JWTError
from passlib.hash import bcrypt
from pydantic import BaseModel, ValidationError
from pydantic import Field

from pyasic_web.auth import AUTH_SCHEME
from .token import TokenData
from pyasic_web.settings import SECRET, ALGORITHM, DEFAULT_DASHBOARD_CARDS, DEFAULT_MINER_CARDS

class User(BaseModel):
    username: str
    name: str = "Anon"
    password: str = "password"
    scopes: list[str] = Field(default_factory=list)
    ip_range: str = "*"
    dashboard_cards: list = Field(default_factory=list)
    miner_cards: list = Field(default_factory=list)

    def get_display_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.username

    def get_hashed_password(self) -> str:
        return self.password

    def get_scopes(self) -> list:
        return self.scopes


class JsonProvider:
    def __init__(self, file):
        self.user_map = {}
        self.file = file
        self.load_users()

    async def find_by_id(self, identifier: str):
        return self.user_map.get(identifier)

    async def find_by_username(self, username_or_email: str):
        return self.user_map.get(username_or_email)

    async def find_by_token(self, token: str):
        return self.user_map.get(token)

    async def find_by_api_key(self, api_key: str):
        if any([user for user in self.user_map.values() if user.api_key == api_key]):
            return [user for user in self.user_map.values() if user.api_key == api_key][
                0
            ]

    def load_users(self):
        if not os.path.exists(self.file):
            open(self.file, "w").close()
        with open(self.file, "r") as f:
            try:
                users_data = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                self.add_user(
                    "admin",
                    "Admin",
                    "pass",
                    ["admin"],
                    "*"
                )
                return

        for u in users_data:
            dashboard_cards = users_data[u].get("dashboard_cards")
            if not dashboard_cards:
                dashboard_cards = DEFAULT_DASHBOARD_CARDS
            miner_cards = users_data[u].get("miner_cards")
            if not miner_cards:
                miner_cards = DEFAULT_MINER_CARDS
            self.user_map[u] = User(
                username=users_data[u]["username"],
                name=users_data[u]["name"],
                password=users_data[u]["password"],
                scopes=users_data[u]["scopes"],
                ip_range=users_data[u]["ip_range"],
                dashboard_cards=dashboard_cards,
                miner_cards=miner_cards,
            )

    def add_user(
        self, username: str, name: str, password: str, scopes: list, ip_range: str
    ):
        self.user_map[username] = User(
            username=username,
            name=name,
            password=bcrypt.hash(password),
            scopes=scopes,
            ip_range=ip_range,
            dashboard_cards=DEFAULT_DASHBOARD_CARDS,
            miner_cards=DEFAULT_MINER_CARDS,
        )
        self.dump_users()

    def delete_user(self, uid):
        self.user_map.pop(uid)
        self.dump_users()

    def update_user_cards(self, user: User):
        if not user.username in self.user_map:
            return
        self.user_map[user.username] = user
        self.dump_users()

    def update_user(
        self,
        username: str,
        name: str,
        scopes: list,
        ip_range: str,
        password: str = None,
    ):
        if not username in self.user_map:
            return
        old_user = self.user_map[username]
        if not password:
            password = old_user.get_hashed_password()
        else:
            password = bcrypt.hash(password)
        new_user = User(
            username=username,
            name=name,
            password=password,
            scopes=scopes,
            ip_range=ip_range,
            dashboard_cards=old_user.dashboard_cards,
            miner_cards=old_user.miner_cards,
        )
        self.user_map[username] = new_user  # noqa
        self.dump_users()

    def dump_users(self):
        user_data = copy(self.user_map)
        for u in user_data:
            user_data[u] = user_data[u].dict()
        with open(self.file, "w") as f:
            f.write(json.dumps(user_data))

    async def verify(self, username: str, password: str) -> Optional[User]:
        user = await self.find_by_username(username_or_email=username)
        if user:
            if bcrypt.verify(password, user.password):
                return user



async def get_current_user(security_scopes: SecurityScopes, token: Annotated[str, Depends(AUTH_SCHEME)]):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = await user_provider.find_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=401,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


user_provider = JsonProvider(os.path.join(os.path.dirname(__file__), "users.json"))
user_provider.dump_users()
