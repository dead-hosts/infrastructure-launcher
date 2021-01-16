"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the updater of the PyFunceble configuration.

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

import importlib.resources
import logging
import os
from typing import Optional

from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.file import FileHelper
from PyFunceble.helpers.merge import Merge

import dead_hosts.launcher.defaults.links
import dead_hosts.launcher.defaults.paths
import dead_hosts.launcher.defaults.pyfunceble
from dead_hosts.launcher.info_manager import InfoManager
from dead_hosts.launcher.updater.base import UpdaterBase


class PyFuncebleConfigUpdater(UpdaterBase):
    """
    Provides the updated of the PyFunceble configuration.
    """

    def __init__(self, info_manager: InfoManager) -> None:
        self.pyfunceble_config_file_instance = FileHelper(
            os.path.join(info_manager.PYFUNCEBLE_CONFIG_DIR, ".PyFunceble.yaml")
        )

        super().__init__(info_manager)

    @property
    def authorized(self) -> bool:
        return not self.info_manager.own_management

    @staticmethod
    def get_commit_message(message: str, ping: Optional[str] = None) -> str:
        """
        Provides the commit message to use.
        """

        if ping:
            return f"{message} | cc {ping} | "
        return message

    def pre(self) -> "PyFuncebleConfigUpdater":
        logging.info(
            "Started to update %r.",
            self.pyfunceble_config_file_instance.path,
        )

        return self

    def post(self) -> "PyFuncebleConfigUpdater":
        logging.info(
            "Finished to update %r",
            self.pyfunceble_config_file_instance.path,
        )

        return self

    def start(self) -> "PyFuncebleConfigUpdater":
        with importlib.resources.path(
            "PyFunceble.data.infrastructure", ".PyFunceble_production.yaml"
        ) as file_path:
            local_version = DictHelper(
                DictHelper().from_yaml_file(str(file_path))
            ).flatten()

        local_version = Merge(
            dead_hosts.launcher.defaults.pyfunceble.CONFIGURATION
        ).into(local_version, strict=True)

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

        if self.info_manager.ping:
            logging.info("Ping names given, appending them to the commit message.")

            local_version[
                "cli_testing.ci.end_commit_message"
            ] = self.get_commit_message(
                local_version["cli_testing.ci.end_commit_message"],
                ping=self.info_manager.get_ping_for_commit(),
            )

        local_version = Merge(
            dead_hosts.launcher.defaults.pyfunceble.PERSISTENT_CONFIG
        ).into(local_version, strict=True)

        if FileHelper(
            os.path.join(
                self.info_manager.WORKSPACE_DIR,
                dead_hosts.launcher.defaults.paths.EXAMPLE_INFO_FILENAME,
            )
        ).exists():
            local_version["cli_testing.ci.active"] = False
            # Default behavior of PyFunceble since 4.0.0b12.
            local_version["cli_testing.autocontinue"] = False

        local_version = DictHelper(local_version).unflatten()

        DictHelper(local_version).to_yaml_file(
            self.pyfunceble_config_file_instance.path
        )

        logging.debug("Configuration:\n%s", self.pyfunceble_config_file_instance.read())

        return self
