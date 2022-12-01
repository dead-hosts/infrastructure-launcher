"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the 'info.json' manager.

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

import copy
import logging
import os
from datetime import datetime, timedelta
from typing import Any

from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.file import FileHelper

import dead_hosts.launcher.defaults.envs
import dead_hosts.launcher.defaults.paths


class InfoManager:
    """
    Provides an interface for the management of the :code:`info.json` file.

    .. warning::
        Keep in mind that this interface provides everything that may be
        needed by other interfaces.
    """

    WORKSPACE_DIR: str = dead_hosts.launcher.defaults.envs.WORKSPACE_DIR
    PYFUNCEBLE_CONFIG_DIR: str = (
        dead_hosts.launcher.defaults.paths.PYFUNCEBLE_CONFIG_DIRECTORY
    )
    GHA_WORKFLOWS_DIR: str = os.path.join(
        WORKSPACE_DIR, dead_hosts.launcher.defaults.paths.GHA_WORKFLOW_DIR
    )

    INFO_FILE = os.path.join(
        WORKSPACE_DIR, dead_hosts.launcher.defaults.paths.INFO_FILENAME
    )

    def __init__(self) -> None:
        self.info_file_instance = FileHelper(self.INFO_FILE)

        if self.info_file_instance.exists():
            self.content = DictHelper().from_json_file(self.info_file_instance.path)
        else:
            self.content = {}

        logging.debug("Administration file path: %r", self.INFO_FILE)
        logging.debug(
            "Administration file exists: %r", self.info_file_instance.exists()
        )
        logging.debug("Administration file content:\n%r", self.content)

        self.update()
        self.create_missing_index()
        self.clean()
        self.store()

    def __getattr__(self, index: str) -> Any:
        if index in self.content:
            return self.content[index]

        raise AttributeError(index)

    def __getitem__(self, index: str) -> Any:
        if index in self.content:
            return self.content[index]

        raise AttributeError(index)

    def __setitem__(self, index: str, value: Any):
        self.content[index] = value

    def __del__(self):
        self.store()

    def store(self) -> "InfoManager":
        """
        Stores the current state.
        """

        local_copy = {}

        for index, value in self.content.items():
            if index.endswith("_timestamp") and isinstance(value, datetime):
                local_copy[index] = value.timestamp()
            elif index.endswith("_datetime") and isinstance(value, datetime):
                local_copy[index] = value.isoformat()
            else:
                local_copy[index] = copy.deepcopy(value)

        DictHelper(local_copy).to_json_file(self.info_file_instance.path)
        return self

    def clean(self) -> "InfoManager":
        """
        Cleans the unneeded indexes.
        """

        for index in [
            "arguments",
            "clean_list_file",
            "clean_original",
            "commit_autosave_message",
            "last_test",
            "list_name",
            "stable",
        ]:
            if index in self.content:
                del self.content[index]

                logging.debug(
                    "Deleted the %r index of the administration file, "
                    "it is not needed anymore.",
                    index,
                )

        return self

    def create_missing_index(self) -> "InfoManager":
        """
        Creates the missing indexes.
        """

        default_datetime = datetime.utcnow() - timedelta(days=15)

        indexes = {
            "currently_under_test": False,
            "custom_pyfunceble_config": {},
            "days_until_next_test": 2,
            "finish_datetime": default_datetime,
            "finish_timestamp": default_datetime.timestamp(),
            "last_download_datetime": default_datetime,
            "last_download_timestamp": default_datetime.timestamp(),
            "latest_part_finish_timestamp": default_datetime.timestamp(),
            "latest_part_start_timestamp": default_datetime.timestamp(),
            "latest_part_finish_datetime": default_datetime,
            "latest_part_start_datetime": default_datetime,
            "name": dead_hosts.launcher.defaults.paths.GIT_BASE_NAME,
            "repo": f"{dead_hosts.launcher.defaults.paths.GIT_REPO_OWNER}/"
            f"{dead_hosts.launcher.defaults.paths.GIT_BASE_NAME}",
            "own_management": False,
            "ping": [],
            "raw_link": None,
            "start_datetime": default_datetime,
            "start_timestamp": default_datetime.timestamp(),
            "live_update": True,
        }

        for index, value in indexes.items():
            if index not in self.content:
                self.content[index] = value

                logging.debug(
                    "Created the %r index of the administration file, "
                    "it was not found.",
                    index,
                )

    def update(self) -> "InfoManager":
        """
        Updates and filters the new content.
        """

        # pylint: disable=too-many-branches

        self.content["name"] = dead_hosts.launcher.defaults.paths.GIT_BASE_NAME

        logging.debug("Updated the `name` index of the administration file.")

        to_delete = [
            FileHelper(os.path.join(self.WORKSPACE_DIR, ".administrators")),
            FileHelper(os.path.join(self.WORKSPACE_DIR, "update_me.py")),
            FileHelper(os.path.join(self.WORKSPACE_DIR, "admin.py")),
        ]

        if "list_name" in self.content:
            to_delete.append(
                FileHelper(os.path.join(self.WORKSPACE_DIR, self.content["list_name"]))
            )

        if "ping" in self.content:
            local_ping_result = []

            for username in self.content["ping"]:
                if username.startswith("@"):
                    local_ping_result.append(username)
                else:
                    local_ping_result.append(f"@{username}")

            self.content["ping"] = local_ping_result

            logging.debug(
                "Updated the `ping` index of the administration file, "
                "the format has to stay the same everywhere."
            )

        if (
            "raw_link" in self.content
            and isinstance(self.content["raw_link"], str)
            and not self.content["raw_link"]
        ):
            self.content["raw_link"] = None

            logging.debug(
                "Updated the `raw_link` index of the administration file, "
                "empty string not accepted."
            )

        if "custom_pyfunceble_config" in self.content:
            if self.content["custom_pyfunceble_config"]:
                if not isinstance(self.content["custom_pyfunceble_config"], dict):
                    self.content["custom_pyfunceble_config"] = {}
                else:
                    self.content["custom_pyfunceble_config"] = DictHelper(
                        self.content["custom_pyfunceble_config"]
                    ).flatten()
            else:
                self.content["custom_pyfunceble_config"] = {}

            logging.debug(
                "Updated the `custom_pyfunceble_config` index of the "
                "administration file, it should be a %r.",
                dict,
            )

        if (
            "custom_pyfunceble_config" in self.content
            and self.content["custom_pyfunceble_config"]
            and not isinstance(self.content["custom_pyfunceble_config"], dict)
        ):
            self.content["custom_pyfunceble_config"] = {}

            logging.debug(
                "Updated the `custom_pyfunceble_config` index of the "
                "administration file, it should be a %r.",
                dict,
            )

        for index in ["currently_under_test"]:
            if index in self.content and not isinstance(self.content[index], bool):
                self.content[index] = bool(int(self.content[index]))

                logging.debug(
                    "Updated the %r index of the administration file, "
                    "it should be a %r.",
                    index,
                    bool,
                )

        for index in [
            "days_until_next_test",
            "finish_timestamp",
            "last_download_datetime"
            "last_download_timestamp"
            "lastest_part_finish_timestamp",
            "lastest_part_start_timestamp",
            "start_timestamp",
        ]:
            if index in self.content and not isinstance(self.content[index], float):
                self.content[index] = float(self.content[index])

                logging.debug(
                    "Updated the %r index of the administration file, "
                    "it should be a %r.",
                    index,
                    float,
                )

        for index in [
            "finish_timestamp",
            "last_download_timestamp",
            "lastest_part_finish_timestamp",
            "lastest_part_start_timestamp",
            "start_timestamp",
        ]:
            if index in self.content and not isinstance(self.content[index], datetime):
                self.content[index] = datetime.fromtimestamp(self.content[index])

                logging.debug(
                    "Updated the %r index of the administration file, "
                    "the system understands %r only."
                    " (JSON => %s).",
                    index,
                    datetime,
                    dict,
                )

        for index in [
            "finish_datetime",
            "last_download_datetime",
            "lastest_part_finish_datetime",
            "lastest_part_start_datetime",
            "start_datetime",
        ]:
            if index in self.content:
                if self.content[index] and not isinstance(
                    self.content[index], datetime
                ):
                    self.content[index] = datetime.fromisoformat(self.content[index])

                    logging.debug(
                        "Updated the %r index of the administration file, "
                        "the system understands %r only."
                        " (JSON => %r.",
                        index,
                        datetime,
                        dict,
                    )
                else:
                    self.content[index] = datetime.fromtimestamp(0)

                    logging.debug(
                        "Set the %r index of the administration file, "
                        "it was not previously set.",
                        repr(index),
                    )

        self.content["repo"] = (
            f"{dead_hosts.launcher.defaults.paths.GIT_REPO_OWNER}/"
            f"{dead_hosts.launcher.defaults.paths.GIT_BASE_NAME}"
        )

        for file in to_delete:
            if file.exists():
                file.delete()

                logging.debug(
                    "Deleted the %r file, it is not needed anymore.",
                    file.path,
                )

    def get_ping_for_commit(self) -> str:
        """
        Provides the string to append in order to mention the users to ping.
        """

        if "ping" in self.content:
            return " ".join(self.content["ping"])
        return ""
