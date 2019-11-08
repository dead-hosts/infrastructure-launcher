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

    Copyright (c) 2019 Dead Hosts
    Copyright (c) 2019 Nissar Chababy

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
import sys
from datetime import datetime

import PyFunceble
from colorama import Fore, Style
from colorama import init as initiate_colorama

from ..configuration import Paths
from ..configuration import TravisCI as TravisCIConfig
from ..helpers import Command
from ..info import Info
from ..travis_ci import TravisCI
from .authorize import Authorize
from .update import Update


class Orchestration:
    """
    Puts everything together.
    """

    def __init__(self, save=False, end=False, debug=False):
        initiate_colorama(autoreset=True)
        if debug:
            debug_level = logging.DEBUG
        else:
            debug_level = logging.INFO

        logging.basicConfig(
            format="[%(asctime)s::%(levelname)s] %(message)s", level=debug_level
        )

        if TravisCIConfig.build_dir:
            self.working_directory = TravisCIConfig.build_dir
        else:
            self.working_directory = Paths.current_directory

        self.info_manager = Info(self.working_directory)

        logging.info(f"Working directory: {self.working_directory}")

        self.authorize = Authorize(self.info_manager)

        self.origin_file_instance = PyFunceble.helpers.File(
            self.working_directory + Paths.origin_filename
        )
        self.input_file_instance = PyFunceble.helpers.File(
            self.working_directory + Paths.input_filename
        )
        self.output_file_instance = PyFunceble.helpers.File(
            self.working_directory + Paths.output_filename
        )

        logging.info(f"Origin file: {self.origin_file_instance.path}")
        logging.info(f"Input file: {self.input_file_instance.path}")
        logging.info(f"Output file: {self.output_file_instance.path}")

        if not end and not save:
            logging.info(f"Checking authorization to run.")

            if self.authorize.test():
                TravisCI.init_repo()
                Update(self.working_directory, self.info_manager)

                PyFunceble.load_config(generate_directory_structure=False)
                self.fetch_list_to_test()

                self.run_test()
            else:
                logging.info(
                    f"Not authorized to run a test until {datetime.now()} "
                    f"(current time) > {self.authorize.get_test_authorization_time()}"
                )
                sys.exit(0)
        elif save:
            self.run_autosave()
        else:
            self.run_end()

    def fetch_list_to_test(self):
        """
        Provides the latest version of the file to test.
        """

        result = {}
        if self.authorize.refresh():
            logging.info("We are authorized to refresh the lists! Let's do that.")
            logging.info(f"Raw Link: {self.info_manager.raw_link}")

            if self.info_manager.raw_link:
                result["origin"] = PyFunceble.helpers.Download(
                    self.info_manager.raw_link
                ).text()

                logging.info(
                    "Could get the new version of the list. Updating the download time."
                )

                self.info_manager["last_download_datetime"] = datetime.now()
                self.info_manager["last_download_timestamp"] = self.info_manager[
                    "last_download_datetime"
                ].timestamp()
            elif self.origin_file_instance.exists():
                logging.info(
                    f"Raw link not given or is empty. Let's work "
                    "with {self.origin_file_instance.file}."
                )

                result["origin"] = self.origin_file_instance.read()

                logging.info("Emptying the download time.")

                self.info_manager["last_download_datetime"] = datetime.fromtimestamp(0)
                self.info_manager["last_download_timestamp"] = self.info_manager[
                    "last_download_datetime"
                ].timestamp()
            else:
                logging.info(
                    f"Could not find {self.origin_file_instance.path}. "
                    "Generating empty content to test."
                )

                result["origin"] = ""

                logging.info("Emptying the download time.")

                self.info_manager["last_download_datetime"] = datetime.fromtimestamp(0)
                self.info_manager["last_download_timestamp"] = self.info_manager[
                    "last_download_datetime"
                ].timestamp()

            if not self.info_manager["custom_pyfunceble_config"]:
                logging.info("Formatting the list to test.")

                result["input_list"] = []

                for line in result["origin"].splitlines():
                    converted = PyFunceble.converter.File(line).get_converted()

                    if not converted:
                        continue

                    if isinstance(converted, list):
                        result["input_list"].extend([x for x in converted if x])
                    else:
                        result["input_list"].append(converted)
            else:
                result["input_list"] = result["origin"].splitlines()

            result["input"] = "\n".join(result["input_list"])

            self.origin_file_instance.write(result["origin"], overwrite=True)
            self.input_file_instance.write(result["input"], overwrite=True)

            logging.info(f"Updated {self.origin_file_instance.path}.")
            logging.info(f"Updated {self.input_file_instance.path}.")

            PyFunceble.output.Clean()
            logging.info("Cleaned the `output` directory of PyFunceble.")
            PyFunceble.output.Constructor()
            logging.info(
                "Ensured that the directory structure of PyFunceble is still valid."
            )

        return result

    def run_test(self):
        """
        Run a test of the input list.
        """

        TravisCI.update_permissions()

        if not self.info_manager.currently_under_test:
            self.info_manager["currently_under_test"] = True

            self.info_manager["start_datetime"] = datetime.now()
            self.info_manager["start_timestamp"] = self.info_manager[
                "start_datetime"
            ].timestamp()

            self.info_manager["finish_datetime"] = datetime.fromtimestamp(0)
            self.info_manager["finish_timestamp"] = self.info_manager[
                "finish_datetime"
            ].timestamp()

        self.info_manager["latest_part_start_datetime"] = datetime.now()
        self.info_manager["latest_part_start_timestamp"] = self.info_manager[
            "latest_part_start_datetime"
        ].timestamp()

        self.info_manager["latest_part_finish_datetime"] = datetime.fromtimestamp(0)
        self.info_manager["latest_part_finish_timestamp"] = self.info_manager[
            "latest_part_finish_datetime"
        ].timestamp()

        logging.info("Updated all timestamps.")
        logging.info(f"Starting PyFunceble {PyFunceble.VERSION} ...")

        PyFunceble.helpers.Command(
            f"PyFunceble -f {self.input_file_instance.path}"
        ).run_to_stdout()

        if not TravisCIConfig.github_token or not TravisCIConfig.build_dir:
            self.run_end()

    def run_autosave(self):
        """
        Run the autosave logic of the administration file.

        .. warning::
            This is just about the administration file not PyFunceble.
        """

        TravisCI.update_permissions()

        self.info_manager["latest_part_finish_datetime"] = datetime.now()
        self.info_manager["latest_part_finish_timestamp"] = self.info_manager[
            "latest_part_finish_datetime"
        ].timestamp()

        logging.info("Updated all timestamps.")

        PyFunceble.helpers.Directory(self.working_directory + "db_types").delete()

        TravisCI.update_permissions()

    def run_end(self):
        """
        Run the end logic.
        """

        self.info_manager["currently_under_test"] = False

        self.info_manager["latest_part_finish_datetime"] = datetime.now()
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

        TravisCI.update_permissions()

        pyfunceble_active_list = PyFunceble.helpers.File(
            self.working_directory + "output/domains/ACTIVE/list"
        )
        clean_list = [
            "# File generated by the Dead-Hosts project with the help of PyFunceble.",
            "# Dead-Hosts: https://github.com/dead-hosts",
            "# PyFunceble: https://pyfunceble.github.io",
            f"# Generation Time: {datetime.now().isoformat()}",
        ]

        logging.info(f"PyFunceble ACTIVE list output: {pyfunceble_active_list.path}")

        if pyfunceble_active_list.exists():
            logging.info(
                f"{pyfunceble_active_list.path} exists, getting and formatting its content."
            )

            clean_list.extend(
                PyFunceble.helpers.List(
                    PyFunceble.helpers.Regex(r"^#").get_not_matching_list(
                        pyfunceble_active_list.read().splitlines()
                    )
                ).format()
            )

        self.output_file_instance.write("\n".join(clean_list), overwrite=True)
        logging.info(f"Updated of the content of {self.output_file_instance.path}")

        PyFunceble.helpers.Directory(self.working_directory + "db_types").delete()

        TravisCI.update_permissions()
