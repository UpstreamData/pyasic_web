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

import os

import toml


def get_current_settings():
    try:
        with open(
            os.path.join(os.path.dirname(__file__), "web_settings.toml"), "r"
        ) as settings_file:
            settings = toml.loads(settings_file.read())
    except:
        settings = {
            "data_sleep_time": 1,
            "miner_data_timeout": 5,
            "miner_identify_timeout": 5,
        }
    return settings


def update_settings(settings):
    with open(
        os.path.join(os.path.dirname(__file__), "web_settings.toml"), "w"
    ) as settings_file:
        settings_file.write(toml.dumps(settings))
