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

    Copyright (c) 2019, 2020, 2021, 2022, 2023, 2024 Dead Hosts Contributors
    Copyright (c) 2019, 2020. 2021, 2022, 2023, 2024 Nissar Chababy

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

import json
import logging
import os
import re

from PyFunceble.helpers.download import DownloadHelper
from PyFunceble.helpers.file import FileHelper
from PyFunceble.helpers.hash import HashHelper

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
            and dead_hosts.launcher.defaults.paths.GIT_BASE_NAME != "template"
        )

    def pre(self) -> "GHAWorkflowsUpdater":
        logging.info("Started to update %r!", self.info_manager.GHA_WORKFLOWS_DIR)

        return self

    def post(self) -> "GHAWorkflowsUpdater":
        logging.info("Trying to randomize the GitHub Actions workflows.")

        files = [
            os.path.join(
                self.info_manager.GHA_WORKFLOWS_DIR,
                dead_hosts.launcher.defaults.links.GHA_MAIN_WORKFLOW["destination"],
            ),
            os.path.join(
                self.info_manager.GHA_WORKFLOWS_DIR,
                dead_hosts.launcher.defaults.links.GHA_SCHEDULER_WORKFLOW[
                    "destination"
                ],
            ),
            os.path.join(
                self.info_manager.GHA_WORKFLOWS_DIR,
                dead_hosts.launcher.defaults.links.GHA_WORKER_WORKFLOW["destination"],
            ),
        ]

        hashes_file = os.path.join(
            self.info_manager.GHA_WORKFLOWS_DIR,
            dead_hosts.launcher.defaults.paths.GHA_WORKFLOW_LOCAL_HASHES_FILENAME,
        )

        if FileHelper(hashes_file).exists():
            hashes_data = json.loads(FileHelper(hashes_file).read())
        else:
            hashes_data = {}

        for file in files:
            filename = os.path.basename(file)
            file_hash = HashHelper().hash_file(file)

            if filename not in hashes_data:
                hashes_data[filename] = file_hash
            elif hashes_data[filename] != file_hash:
                hashes_data[filename] = file_hash
            else:
                logging.info("Skipping %r because it was not modified.", filename)
                continue

            with open(file, "r", encoding="utf-8") as file_stream:
                content = file_stream.read()

                try:
                    current_cron = re.search(r"cron: \"(.*?)\"", content).group(1)

                    if current_cron:
                        new_cron = self.randomize_cron(current_cron)
                        content = content.replace(current_cron, new_cron)

                        logging.info("Randomized %r to %r", current_cron, new_cron)
                except AttributeError:
                    pass

            with open(file, "w", encoding="utf-8") as file_stream:
                file_stream.write(content)

        FileHelper(hashes_file).write(json.dumps(hashes_data, indent=2), overwrite=True)

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

        DownloadHelper(
            dead_hosts.launcher.defaults.links.GHA_WORKER_WORKFLOW["link"]
        ).download_text(
            destination=os.path.join(
                self.info_manager.GHA_WORKFLOWS_DIR,
                dead_hosts.launcher.defaults.links.GHA_WORKER_WORKFLOW["destination"],
            )
        )

        return self
