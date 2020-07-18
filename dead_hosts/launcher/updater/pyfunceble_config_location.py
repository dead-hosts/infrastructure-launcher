"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the updater of the location of the PyFunceble configuration files.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Project link:
    https://github.com/dead-hosts/infrastructure-launcher

License:
::

    MIT License

    Copyright (c) 2019, 2020 Dead Hosts
    Copyright (c) 2019, 2020 Nissar Chababy

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

import logging

import PyFunceble.helpers as pyfunceble_helpers

from .base import Base


class PyFuncebleConfigLocationUpdater(Base):
    """
    Provides the updater of the location of the PyFunceble configuration files.
    """

    files_to_move: str = [
        ".pyfunceble_intern_downtime.json",
        ".PyFunceble_production.yaml",
        ".PyFunceble.yaml",
        "dir_structure.json",
        "hashes_tracker.json",
        "iana-domains-db.json",
        "inactive_db.json",
        "public-suffix.json",
        "user_agents.json",
        "whois_db.json",
    ]

    def authorization(self) -> bool:
        if not pyfunceble_helpers.Directory(self.pyfunceble_config_dir).exists():
            return True

        for file in self.files_to_move:
            if pyfunceble_helpers.File(self.working_dir + file).exists():
                return True

        return False

    def pre(self) -> None:
        logging.info(
            "Started to move files into %s.", self.pyfunceble_config_dir,
        )

        directory_to_create = pyfunceble_helpers.Directory(self.pyfunceble_config_dir)

        logging.info("Ensure that %s exists", directory_to_create.path)
        directory_to_create.create()

    def post(self) -> None:
        logging.info(
            "Finished to move files into %s.", self.pyfunceble_config_dir,
        )

    def start(self) -> None:
        for file in self.files_to_move:
            logging.info(
                "Starting to move %s into %s.", file, self.pyfunceble_config_dir
            )
            pyfunceble_helpers.File(self.working_dir + file).move(
                self.pyfunceble_config_dir + file
            )
            logging.info(
                "Finished to move %s into %s", file, self.pyfunceble_config_dir
            )
