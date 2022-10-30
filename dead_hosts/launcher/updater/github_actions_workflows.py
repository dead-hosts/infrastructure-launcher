"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the updater of the GitHub actions workflow.

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

from PyFunceble.helpers.download import DownloadHelper
from PyFunceble.helpers.file import FileHelper

import dead_hosts.launcher.defaults.envs
import dead_hosts.launcher.defaults.links
import dead_hosts.launcher.defaults.paths
from dead_hosts.launcher.updater.base import UpdaterBase


class GHAWorkflowsUpdater(UpdaterBase):
    """
    Provides the updater of the GitHub Actions workflows.
    """

    @property
    def authorized(self) -> bool:
        return (
            dead_hosts.launcher.defaults.envs.UNDER_CI
            and not FileHelper(
                os.path.join(
                    self.info_manager.WORKSPACE_DIR,
                    dead_hosts.launcher.defaults.paths.EXAMPLE_INFO_FILENAME,
                )
            ).exists()
        )

    def pre(self) -> "GHAWorkflowsUpdater":
        logging.info("Started to update %r!", self.info_manager.GHA_WORKFLOWS_DIR)

        return self

    def post(self) -> "GHAWorkflowsUpdater":
        logging.info("Finished to update %r!", self.info_manager.GHA_WORKFLOWS_DIR)

        return self

    def start(self) -> "GHAWorkflowsUpdater":
        DownloadHelper(
            dead_hosts.launcher.defaults.links.GHA_MAIN_WORKFLOW["link"]
        ).download_text(
            destination=os.path.join(
                self.info_manager.GHA_WORKFLOWS_DIR,
                dead_hosts.launcher.defaults.links.GHA_MAIN_WORKFLOW["destination"],
            )
        )

        DownloadHelper(
            dead_hosts.launcher.defaults.links.GHA_SCHEDULER_WORKFLOW["link"]
        ).download_text(
            destination=os.path.join(
                self.info_manager.GHA_WORKFLOWS_DIR,
                dead_hosts.launcher.defaults.links.GHA_SCHEDULER_WORKFLOW[
                    "destination"
                ],
            )
        )

        return self
