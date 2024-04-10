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

from pathlib import Path

BASE_DIR = Path(__file__).parent

TEMPLATES_DIR = BASE_DIR.joinpath("templates")
STATIC_DIR = BASE_DIR.joinpath("static")
MINER_LIST = BASE_DIR.joinpath("miners.json")
MINER_PHASE_LIST = BASE_DIR.joinpath("phases.json")

SECRET = "SECRET"
ALGORITHM = "HS256"

DEFAULT_DASHBOARD_CARDS = [
    "count",
    "hashrate",
    "hashrate-graph",
    "expected_hashrate",
    "pct_expected_hashrate",
    "wattage-graph",
    "wattage",
    "max_wattage",
    "pct_expected_wattage",
    "efficiency",
    "temperature_avg",
    "env_temp",
    "temperature_avg-graph",
    "expected_chips",
    "total_chips",
    "efficiency-graph",
    "errors",
]
DEFAULT_MINER_CARDS = [
    "model",
    "api_ver",
    "make",
    "fw_ver",
    "hashrate-graph",
    "temperature_avg-graph",
    "hashrate",
    "efficiency",
    "wattage",
    "pct_expected_hashrate",
]
