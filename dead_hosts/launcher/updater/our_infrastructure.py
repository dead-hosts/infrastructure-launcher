"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the updater of our infrastructure files.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Project link:
    https://github.com/dead-hosts/infrastructure-launcher

License:
::

    MIT License

    Copyright (c) 2019, 2020, 2021, 2022 Dead Hosts
    Copyright (c) 2019, 2020. 2021, 2022 Nissar Chababy

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

import dead_hosts.launcher.defaults.paths
from dead_hosts.launcher.updater.base import UpdaterBase


class OurInfrastructureUpdater(UpdaterBase):
    """
    Provides the updated of our infrastructure files.
    """

    FILES_TO_REMOVE = [
        dead_hosts.launcher.defaults.paths.INPUT_FILENAME,
        ".pyfunceble_intern_downtime.json",
        "dir_structure.json",
        "iana-domains-db.json",
        "public-suffix.json",
        "pyfunceble.db",
        ".travis.yml",
        os.path.join("output", "continue.json"),
        ".PyFunceble_cross_repositories_config.yaml",
    ]

    DIRS_TO_REMOVE = [
        "db_types",
        os.path.join("output", "Analytic"),
        os.path.join("output", "domains"),
        os.path.join("output", "hosts"),
        os.path.join("output", "json"),
        os.path.join("output", "logs"),
        os.path.join("output", "splited"),
        os.path.join("output", "complements"),
    ]

    @property
    def authorized(self) -> bool:
        return any(
            FileHelper(os.path.join(self.info_manager.WORKSPACE_DIR, x)).exists()
            for x in self.FILES_TO_REMOVE
        ) or any(
            DirectoryHelper(os.path.join(self.info_manager.WORKSPACE_DIR, x)).exists()
            for x in self.DIRS_TO_REMOVE
        )

    def pre(self) -> "OurInfrastructureUpdater":
        logging.info("Started maintenance of %r.", self.info_manager.WORKSPACE_DIR)

        return self

    def post(self) -> "OurInfrastructureUpdater":
        logging.info("Finished maintenance of %r", self.info_manager.WORKSPACE_DIR)

        return self

    def start(self) -> "OurInfrastructureUpdater":

        file_helper = FileHelper()
        dir_helper = DirectoryHelper()

        for file in self.FILES_TO_REMOVE:
            file_helper.set_path(os.path.join(self.info_manager.WORKSPACE_DIR, file))

            if file_helper.exists():
                logging.info("Starting deletion of %r", file_helper.path)

                file_helper.delete()

                logging.info("Finished deletion of %r", file_helper.path)

        for directory in self.DIRS_TO_REMOVE:
            dir_helper.set_path(
                os.path.join(self.info_manager.WORKSPACE_DIR, directory)
            )

            if dir_helper.exists():
                logging.info("Starting deletion of %r", dir_helper.path)

                dir_helper.delete()

                logging.info("Finished deletion of %r", dir_helper.path)

        return self
