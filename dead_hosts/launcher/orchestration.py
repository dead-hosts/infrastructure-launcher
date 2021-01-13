"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the orchestration logic. In other words, put everything
together to process a test.

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
import sys
from datetime import datetime
from typing import Optional

import PyFunceble
import PyFunceble.facility
from PyFunceble.helpers.download import DownloadHelper
from PyFunceble.helpers.environment_variable import EnvironmentVariableHelper
from PyFunceble.helpers.file import FileHelper

import dead_hosts.launcher.defaults.envs
import dead_hosts.launcher.defaults.paths
from dead_hosts.launcher.authorization import Authorization
from dead_hosts.launcher.command import Command
from dead_hosts.launcher.info_manager import InfoManager
from dead_hosts.launcher.updater.all import execute_all_updater


class Orchestration:
    """
    Orchester the test launch.
    """

    info_manager: Optional[InfoManager] = None
    authorization_handler: Optional[Authorization] = None

    origin_file: Optional[FileHelper] = None
    output_file: Optional[FileHelper] = None

    def __init__(self, save: bool = False, end: bool = False) -> None:

        self.info_manager = InfoManager()

        git_name = EnvironmentVariableHelper("GIT_NAME")
        git_email = EnvironmentVariableHelper("GIT_EMAIL")

        if git_email.exists() and "funilrys" in git_email.get_value():
            git_name.set_value(dead_hosts.launcher.defaults.envs.GIT_NAME)
            git_email.set_value(dead_hosts.launcher.defaults.envs.GIT_EMAIL)

        EnvironmentVariableHelper("PYFUNCEBLE_OUTPUT_LOCATION").set_value(
            self.info_manager.WORKSPACE_DIR
        )

        EnvironmentVariableHelper("PYFUNCEBLE_CONFIG_DIR").set_value(
            self.info_manager.PYFUNCEBLE_CONFIG_DIR
        )

        self.authorization_handler = Authorization(self.info_manager)

        self.origin_file = FileHelper(
            os.path.join(
                self.info_manager.WORKSPACE_DIR,
                dead_hosts.launcher.defaults.paths.ORIGIN_FILENAME,
            )
        )

        self.output_file = FileHelper(
            os.path.join(
                self.info_manager.WORKSPACE_DIR,
                dead_hosts.launcher.defaults.paths.OUTPUT_FILENAME,
            )
        )

        logging.info("Origin file: %r", self.origin_file.path)
        logging.info("Output file: %r", self.output_file.path)

        if not end and not save:
            logging.info("Checking authorization to run.")

            if self.authorization_handler.is_test_authorized():
                execute_all_updater(self.info_manager)

                PyFunceble.facility.ConfigLoader.start()
                self.fetch_file_to_test()

                self.run_test()
            else:
                logging.info(
                    "Not authorized to run a test until %r (current time) > %r",
                    datetime.now(),
                    self.authorization_handler.next_authorization_time,
                )
                sys.exit(0)
        elif save:
            self.run_autosave()
        else:
            self.run_end()

    def fetch_file_to_test(self) -> "Orchestration":
        """
        Provides the latest version of the file to test.
        """

        if self.authorization_handler.is_refresh_authorized():
            logging.info("We are authorized to refresh the lists! Let's do that.")
            logging.info("Raw Link: %r", self.info_manager.raw_link)

            if self.info_manager.raw_link:
                DownloadHelper(self.info_manager.raw_link).download_text(
                    destination=self.origin_file.path
                )

                logging.info(
                    "Could get the new version of the list. Updating the download time."
                )

                self.info_manager["last_download_datetime"] = datetime.utcnow()
                self.info_manager["last_download_timestamp"] = self.info_manager[
                    "last_download_datetime"
                ].timestamp()
            elif self.origin_file.exists():
                logging.info(
                    "Raw link not given or is empty. Let's work with %r.",
                    self.origin_file.path,
                )

                self.origin_file.read()

                logging.info("Emptying the download time.")

                self.info_manager["last_download_datetime"] = datetime.fromtimestamp(0)
                self.info_manager["last_download_timestamp"] = self.info_manager[
                    "last_download_datetime"
                ].timestamp()
            else:
                logging.info(
                    f"Could not find {self.origin_file.path}. "
                    "Generating empty content to test."
                )

                self.origin_file.write("# No content yet.", overwrite=True)

                logging.info("Emptying the download time.")

                self.info_manager["last_download_datetime"] = datetime.fromtimestamp(0)
                self.info_manager["last_download_timestamp"] = self.info_manager[
                    "last_download_datetime"
                ].timestamp()

            logging.info("Updated %r.", self.origin_file.path)

        return self

    def run_test(self):
        """
        Run a test of the input list.
        """

        if not self.info_manager.currently_under_test:
            self.info_manager["currently_under_test"] = True

            self.info_manager["start_datetime"] = datetime.utcnow()
            self.info_manager["start_timestamp"] = self.info_manager[
                "start_datetime"
            ].timestamp()

            self.info_manager["finish_datetime"] = datetime.fromtimestamp(0)
            self.info_manager["finish_timestamp"] = self.info_manager[
                "finish_datetime"
            ].timestamp()

        self.info_manager["latest_part_start_datetime"] = datetime.utcnow()
        self.info_manager["latest_part_start_timestamp"] = self.info_manager[
            "latest_part_start_datetime"
        ].timestamp()

        self.info_manager["latest_part_finish_datetime"] = datetime.fromtimestamp(0)
        self.info_manager["latest_part_finish_timestamp"] = self.info_manager[
            "latest_part_finish_datetime"
        ].timestamp()

        logging.info("Updated all timestamps.")
        logging.info("Starting PyFunceble %r ...", PyFunceble.__version__)

        Command(f"PyFunceble -f {self.origin_file.path}").run_to_stdout()

        if not dead_hosts.launcher.defaults.envs.GITHUB_TOKEN:
            self.run_end()

    def run_autosave(self):
        """
        Run the autosave logic of the administration file.

        .. warning::
            This is just about the administration file not PyFunceble.
        """

        self.info_manager["latest_part_finish_datetime"] = datetime.utcnow()
        self.info_manager["latest_part_finish_timestamp"] = self.info_manager[
            "latest_part_finish_datetime"
        ].timestamp()

        logging.info("Updated all timestamps.")

    def run_end(self):
        """
        Run the end logic.
        """

        self.info_manager["currently_under_test"] = False

        self.info_manager["latest_part_finish_datetime"] = datetime.utcnow()
        self.info_manager["latest_part_finish_timestamp"] = self.info_manager[
            "latest_part_finish_datetime"
        ].timestamp()

        self.info_manager["finish_datetime"] = self.info_manager[
            "latest_part_finish_datetime"
        ]
        self.info_manager["finish_timestamp"] = self.info_manager[
            "finish_datetime"
        ].timestamp()

        logging.info("Updated all timestamps and indexes that needed to be updated.")

        pyfunceble_active_list = FileHelper(
            os.path.join(
                self.info_manager.WORKSPACE_DIR,
                "output",
                dead_hosts.launcher.defaults.paths.ORIGIN_FILENAME,
                "domains",
                "ACTIVE",
                "list",
            )
        )

        clean_list = [
            "# File generated by the Dead-Hosts project with the help of PyFunceble.",
            "# Dead-Hosts: https://github.com/dead-hosts",
            "# PyFunceble: https://pyfunceble.github.io",
            f"# Generation Time: {datetime.utcnow().isoformat()}",
        ]

        logging.info(f"PyFunceble ACTIVE list output: {pyfunceble_active_list.path}")

        if pyfunceble_active_list.exists():
            logging.info(
                f"{pyfunceble_active_list.path} exists, getting and formatting its content."
            )

            self.output_file.write("\n".join(clean_list) + "\n\n", overwrite=True)

            with pyfunceble_active_list.open("r", encoding="utf-8") as file_stream:
                for line in file_stream:
                    if line.startswith("#"):
                        continue

                    self.output_file.write(line)

            self.output_file.write("\n")

            logging.info("Updated of the content of %r", self.output_file.path)
