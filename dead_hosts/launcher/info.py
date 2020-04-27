"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides a direct access and management logic of the administration file
(:code:`info.json´).

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
from datetime import datetime, timedelta

import PyFunceble.helpers as pyfunceble_helpers

from .configuration import Paths
from .travis_ci import TravisCI


class Info:
    """
    Provides an interface to manage the `info.json` file.

    :ivar str working_directory:
        Our working directory.
    :ivar str file:
        The full path of the previously known as `info.json` file.
    :ivar file_instance:
        An instance of :py:class`PyFunceble.helpers.File`.
    :vartype file_instance: :py:class`PyFunceble.helpers.File
    :ivar dict content:
        The content of `info.json` (in dict).
    """

    def __init__(self):
        self.working_directory: str = TravisCI.get_working_dir()

        self.file: str = self.working_directory + Paths.info_filename
        self.file_instance: pyfunceble_helpers.File = pyfunceble_helpers.File(self.file)

        if self.file_instance.exists():
            self.content: dict = pyfunceble_helpers.Dict().from_json(
                self.file_instance.read()
            )
        else:
            self.content: dict = {}

        logging.debug("Administration file path: %s", self.file)
        logging.debug("Administration file exists: %s", self.file_instance.exists())
        logging.debug("Administration file content: %s", self.file_instance.read())
        logging.debug("Administration file interpreted: %s", self.content)

        self.filter()
        self.create_missing_index()
        self.clean()
        self.save()

    def __getitem__(self, index):
        if index in self.content:
            return self.content[index]
        raise KeyError(index)

    def __getattr__(self, index):
        if index in self.content:
            return self.content[index]
        raise AttributeError(index)

    def __setitem__(self, index, value):
        self.content[index] = value
        self.save()

    def filter(self):
        """
        Processes a first filtering of the file.
        """

        # pylint: disable=too-many-branches

        self.content["name"] = Paths.git_base_name

        logging.debug("Updated the `name` index of the administration file.")

        to_delete = [
            pyfunceble_helpers.File(self.working_directory + ".administrators"),
            pyfunceble_helpers.File(self.working_directory + "update_me.py"),
            pyfunceble_helpers.File(self.working_directory + "admin.py"),
        ]

        if "list_name" in self.content:
            to_delete.append(
                pyfunceble_helpers.File(
                    self.working_directory + self.content["list_name"]
                )
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

        if (
            "custom_pyfunceble_config" in self.content
            and self.content["custom_pyfunceble_config"]
            and not isinstance(self.content["custom_pyfunceble_config"], dict)
        ):
            self.content["custom_pyfunceble_config"] = {}
            logging.debug(
                "Updated the `custom_pyfunceble_config` index of the "
                "administration file, it should be a %s.",
                dict,
            )

        for file_to_delete in to_delete:
            if file_to_delete.exists():
                file_to_delete.delete()

                logging.debug(
                    "Deleted the %s file, it is not needed anymore.",
                    repr(file_to_delete.path),
                )

        for index in ["currently_under_test"]:
            if index in self.content and not isinstance(self.content[index], bool):
                self.content[index] = bool(int(self.content[index]))

                logging.debug(
                    "Updated the %s index of the administration file, "
                    "it should be a %s.",
                    repr(index),
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
                    "Updated the %s index of the administration file, "
                    "it should be a %s.",
                    repr(index),
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
                    "Updated the %s index of the administration file, "
                    "the system understands %s only."
                    " (JSON => %s).",
                    repr(index),
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
                        "Updated the %s index of the administration file, "
                        "the system understands %s only."
                        " (JSON => %s.",
                        repr(index),
                        datetime,
                        dict,
                    )
                else:
                    self.content[index] = datetime.fromtimestamp(0)
                    logging.debug(
                        "Set the %s index of the administration file, "
                        "it was not previously set.",
                        repr(index),
                    )

    def create_missing_index(self):
        """
        Creates the missing indexes.
        """

        default_datetime = datetime.now() - timedelta(days=10)

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
            "name": Paths.git_base_name,
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
                    "Created the %s index of the administration file, it was not found.",
                    repr(index),
                )

    def clean(self):
        """
        Removes the unneeded indexes.
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
                    "Deleted the %s index of the administration file, "
                    "it is not needed anymore.",
                    repr(index),
                )

    def save(self):
        """
        Saves the current version of the content file.
        """

        origin = self.content.copy()

        for index, value in self.content.copy().items():
            if index.endswith("_timestamp") and isinstance(value, datetime):
                self.content[index] = value.timestamp()
            elif index.endswith("_datetime") and isinstance(value, datetime):
                self.content[index] = value.isoformat()

        pyfunceble_helpers.Dict(self.content).to_json_file(self.file)
        self.content = origin

    def get_ping_for_commit(self):
        """
        Returns the list of username for the commit message.
        """

        if "ping" in self.content:
            return " ".join(self.content["ping"])
        return ""
