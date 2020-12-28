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

from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.download import DownloadHelper
from PyFunceble.helpers.merge import Merge

import dead_hosts.launcher.defaults.links
import dead_hosts.launcher.defaults.paths
import dead_hosts.launcher.defaults.pyfunceble
import dead_hosts.launcher.defaults.travis_ci
from dead_hosts.launcher.updater.cross_pyfunceble_config import (
    CrossPyFuncebleConfigUpdater,
)


class PyFuncebleConfigUpdater(CrossPyFuncebleConfigUpdater):
    """
    Provides the updated of the PyFunceble configuartion.
    """

    @property
    def authorized(self) -> bool:
        return (
            not self.cross_file_instance.exists()
            and not self.info_manager.own_management
        )

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
        upstreamcross_repo_version = DownloadHelper(
            dead_hosts.launcher.defaults.links.CROSS_REPO_PYFUNCEBLE_CONFIG["link"]
        ).download_text()

        upstream_flatten = DictHelper(
            DictHelper().from_yaml(upstreamcross_repo_version)
        ).flatten()

        local_version = Merge(
            dead_hosts.launcher.defaults.pyfunceble.CONFIGURATION
        ).into(upstream_flatten, strict=True)

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

        local_version = Merge(
            dead_hosts.launcher.defaults.pyfunceble.CONFIGURATION
        ).into(local_version, strict=True)
        local_version = DictHelper(local_version).unflatten()

        DictHelper(local_version).to_yaml_file(
            self.pyfunceble_config_file_instance.path
        )

        return self
