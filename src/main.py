# main.py
#
# Copyright 2022 Unknown
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from .parser import Config
from .functions.partitioning import Partitioning

def main(argv):
    if argv[1] == "config":
        config = ""

        with open(argv[2], "r+") as f:
            config = f.read()
            parsed = Config(config=config)

        Partitioning(parsed.get_partition_settings())
        print(parsed.get_bootloader_settings())
        print(parsed.get_locale_settings())
        print(parsed.get_networking_settings())
        print(parsed.get_user_settings())
        print(parsed.get_root_password())
        print(parsed.get_extra_packages())

