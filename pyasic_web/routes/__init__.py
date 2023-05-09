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
from . import dashboard, login, miner, manage
from fastapi import APIRouter

router = APIRouter()

# manual routes
router.add_route("/dashboard", dashboard.dashboard_page)
router.add_route("/login", login.login_page, methods=["POST", "GET"])
router.add_route("/", login.login_page, methods=["POST", "GET"])
router.add_route("/logout", login.logout_page)

# routers
router.include_router(miner.router, prefix="/miner")
router.include_router(manage.router, prefix="/manage")
