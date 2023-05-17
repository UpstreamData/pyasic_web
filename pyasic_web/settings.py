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

TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
MINER_LIST = BASE_DIR / "miner_list.txt"

SECRET = "SECRET"
ALGORITHM = "HS256"

DEFAULT_DASHBOARD_CARDS = [
    "count",
    "hashrate",
    "pct_ideal_chips",
    "temperature_avg",
    "wattage",
    "pct_ideal_wattage",
    "efficiency",
    "errors",
]
DEFAULT_MINER_CARDS = [
    "model",
    "hashrate",
    "pct_ideal_chips",
    "temperature_avg",
    "wattage",
    "pct_ideal_wattage",
    "efficiency",
    "errors",
    "pools",
]
