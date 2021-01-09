"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the updater of our pyfunceble configuration location.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Project link:
    https://github.com/dead-hosts/infrastructure-launcher

License:
::

    MIT License

    Copyright (c) 2019, 2020, 2021 Dead Hosts
    Copyright (c) 2019, 2020. 2021 Nissar Chababy

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
import os

from PyFunceble.helpers.directory import DirectoryHelper
from PyFunceble.helpers.file import FileHelper

from dead_hosts.launcher.updater.base import UpdaterBase


class PyFuncebleConfigLocationUpdater(UpdaterBase):
    """
    Provides the updater of our pyfunceble configuration location.
    """

    FILES_TO_MOVE: str = [
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

    INACTIVE_FILES_TO_DELETE: str = ["inactive_db.json", "inactive.csv"]

    @property
    def authorized(self) -> bool:
        if not DirectoryHelper(self.info_manager.PYFUNCEBLE_CONFIG_DIR).exists():
            return True

        file_helper = FileHelper()
        for file in self.FILES_TO_MOVE:
            if file_helper.set_path(
                os.path.join(self.info_manager.PYFUNCEBLE_CONFIG_DIR, file)
            ).exists():
                return True

        if all(
            file_helper.set_path(
                os.path.join(self.info_manager.PYFUNCEBLE_CONFIG_DIR, x)
            ).exists()
            for x in self.INACTIVE_FILES_TO_DELETE
        ):
            return True

        return False

    def pre(self) -> "PyFuncebleConfigLocationUpdater":
        logging.info(
            "Started maintenance of %r.",
            self.info_manager.PYFUNCEBLE_CONFIG_DIR,
        )

        DirectoryHelper(self.info_manager.PYFUNCEBLE_CONFIG_DIR).create()

        return self

    def post(self) -> "PyFuncebleConfigLocationUpdater":
        logging.info(
            "Finished maintenance %r",
            self.info_manager.PYFUNCEBLE_CONFIG_DIR,
        )

        return self

    def start(self) -> "PyFuncebleConfigLocationUpdater":
        for file in self.FILES_TO_MOVE:
            source_file = FileHelper(
                os.path.join(self.info_manager.WORKSPACE_DIR, file)
            )
            destination_file = FileHelper(
                os.path.join(self.info_manager.PYFUNCEBLE_CONFIG_DIR, file)
            )

            if source_file.exists():
                logging.info(
                    "Starting to move %r into %r.",
                    source_file.path,
                    destination_file.path,
                )

                destination_file.delete()
                source_file.move(destination_file.path)

                logging.info(
                    "Finished to move %r into %r",
                    source_file.path,
                    destination_file.path,
                )
            else:
                logging.info(
                    "Did not moved move %r into %r: It does not exists.",
                    source_file.path,
                    destination_file.path,
                )

            if (
                all(
                    FileHelper(
                        os.path.join(self.info_manager.PYFUNCEBLE_CONFIG_DIR, x)
                    ).exists()
                    for x in self.INACTIVE_FILES_TO_DELETE
                )
                or FileHelper(
                    os.path.join(
                        self.info_manager.PYFUNCEBLE_CONFIG_DIR,
                        self.INACTIVE_FILES_TO_DELETE[0],
                    )
                ).exists()
            ):
                logging.info(
                    "Starting to delete inactive files.",
                )

                for inactive_file in self.INACTIVE_FILES_TO_DELETE:
                    FileHelper(
                        os.path.join(
                            self.info_manager.PYFUNCEBLE_CONFIG_DIR, inactive_file
                        )
                    ).delete()

                logging.info(
                    "Finished to delete inactive files.",
                )

        return self
