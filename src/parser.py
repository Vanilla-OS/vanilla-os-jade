# parser.py
#
# Copyright 2022 axtloss <axtlos@tar.black>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation version 3 of the License only
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-only

import json

class Config:
    def __init__(self, config):
        self.config = config
        self.parsed_config = json.loads(config)

    def get_partition_settings(self):
        return self.parsed_config["partition"]

    def get_bootloader_settings(self):
        return self.parsed_config["bootloader"]

    def get_locale_settings(self):
        return self.parsed_config["locale"]

    def get_networking_settings(self):
        return self.parsed_config["networking"]

    def get_user_settings(self):
        return self.parsed_config["users"]

    def get_root_password(self):
        return self.parsed_config["rootpass"]

    def get_extra_packages(self):
        return self.parsed_config["extra_packages"]
