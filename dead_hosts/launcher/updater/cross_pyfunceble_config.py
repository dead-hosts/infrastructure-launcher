"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the updater of our cross repository PyFunceble configuration.

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
import os
from typing import Optional

from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.download import DownloadHelper
from PyFunceble.helpers.file import FileHelper
from PyFunceble.helpers.merge import Merge

import dead_hosts.launcher.defaults.links
import dead_hosts.launcher.defaults.paths
import dead_hosts.launcher.defaults.pyfunceble
import dead_hosts.launcher.defaults.travis_ci
from dead_hosts.launcher.info_manager import InfoManager
from dead_hosts.launcher.updater.base import UpdaterBase


class CrossPyFuncebleConfigUpdater(UpdaterBase):
    """
    Provides the updated of our cross-repository PyFunceble configuartion.
    """

    CROSS_CONFIG_FILE: str = os.path.join(
        dead_hosts.launcher.defaults.travis_ci.BUILD_DIR,
        dead_hosts.launcher.defaults.links.CROSS_REPO_PYFUNCEBLE_CONFIG["destination"],
    )

    DESTINATION: str = os.path.join(
        dead_hosts.launcher.defaults.travis_ci.BUILD_DIR, ".PyFunceble.yaml"
    )

    def __init__(self, info_manager: InfoManager) -> None:
        self.cross_file_instance = FileHelper(self.CROSS_CONFIG_FILE)
        self.pyfunceble_config_file_instance = FileHelper(self.DESTINATION)

        super().__init__(info_manager)

    @property
    def authorized(self) -> bool:
        return (
            self.cross_file_instance.exists()
            or not dead_hosts.launcher.defaults.travis_ci.GIT_EMAIL
        )

    @staticmethod
    def get_commit_message(ping: Optional[str] = None) -> str:
        """
        Provides the commit message to use.
        """

        if ping:
            marker = dead_hosts.launcher.defaults.pyfunceble.CONFIGURATION[
                "cli_testing.ci.end_commit_message"
            ]

            return f"{marker} | cc {ping} | "
        return dead_hosts.launcher.defaults.pyfunceble.CONFIGURATION[
            "cli_testing.ci.commit_message"
        ]

    def pre(self) -> "CrossPyFuncebleConfigUpdater":
        logging.info(
            "Started to update %r and %r",
            self.cross_file_instance.path,
            self.pyfunceble_config_file_instance.path,
        )

        return self

    def post(self) -> "CrossPyFuncebleConfigUpdater":
        logging.info(
            "Finished to update %r and %r",
            self.cross_file_instance.path,
            self.pyfunceble_config_file_instance.path,
        )

        return self

    def start(self) -> "CrossPyFuncebleConfigUpdater":
        upstream_data = DownloadHelper(
            dead_hosts.launcher.defaults.links.OFFICIAL_PYFUNCEBLE_CONFIG["link"]
        ).download_text()

        flatten_upstream_version = DictHelper(
            DictHelper().from_yaml(upstream_data)
        ).flatten()

        local_version = Merge(
            dead_hosts.launcher.defaults.pyfunceble.CONFIGURATION
        ).into(flatten_upstream_version, strict=True)

        if self.info_manager.ping:
            logging.info("Ping names given, appending them to the commit message.")

            local_version[
                "cli_testing.ci.end_commit_message"
            ] = self.get_commit_message(ping=self.info_manager.get_ping_for_commit())

        if self.info_manager.custom_pyfunceble_config and isinstance(
            self.info_manager.custom_pyfunceble_config, dict
        ):
            logging.info(
                "Custom PyFunceble configuration given, "
                "appending them to the local configuration file."
            )

            local_version = Merge(self.info_manager.custom_pyfunceble_config).into(
                local_version, strict=True
            )

        local_version = Merge(local_version).into(flatten_upstream_version, strict=True)
        local_version = DictHelper(local_version).unflatten()

        DictHelper(local_version).to_yaml_file(self.cross_file_instance.path)
        DictHelper(local_version).to_yaml_file(
            self.pyfunceble_config_file_instance.path
        )

        return self
