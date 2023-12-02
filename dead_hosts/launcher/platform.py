"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the platform interface.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Project link:
    https://github.com/dead-hosts/infrastructure-launcher

License:
::

    MIT License

    Copyright (c) 2019, 2020, 2021, 2022, 2023 Dead Hosts
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
import tempfile
from typing import Optional

import requests
from PyFunceble.helpers.environment_variable import EnvironmentVariableHelper
from PyFunceble.helpers.file import FileHelper

import dead_hosts.launcher.defaults.paths
from dead_hosts.launcher.info_manager import InfoManager


class PlatformOrchestration:
    """
    Provides the platform interface.
    """

    DEFAULT_API_URL = "https://api.example.com"

    _api_url = DEFAULT_API_URL
    __cached_header: dict = {}

    info_manager: InfoManager
    headers: dict = {}
    session: requests.Session

    def __init__(self, info_manager: InfoManager) -> None:
        self.info_manager = info_manager

        self.api_url = EnvironmentVariableHelper("DEV_PLATFORM_API_URL").get_value(
            default=self.DEFAULT_API_URL
        )

        api_token = EnvironmentVariableHelper("DEV_PLATFORM_API_TOKEN").get_value(
            default=None
        )

        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)

    @property
    def api_url(self) -> str:
        """
        Provides the API URL to use.
        """

        return self._api_url

    @api_url.setter
    def api_url(self, value: str) -> None:
        """
        Sets the API URL to use.
        """

        self._api_url = value.rstrip("/")

    @property
    def container_canonical_data(self) -> dict:
        """
        Provides the canonical data of the container.
        """

        return {
            "availability_test": True,
            "reputation_test": False,
            "syntax_test": True,
            "shortname": self.info_manager.platform_shortname,
            "name": self.info_manager.name,
            "description": self.info_manager.platform_description,
            "public": True,
            "subject_type": "domain",
        }

    @property
    def remote_source_canonical_data(self) -> dict:
        """
        Provides the canonical data of the remote source.
        """

        if self.info_manager.raw_link:
            url = self.info_manager.raw_link
        else:
            url = (
                "https://raw.githubusercontent.com"
                f"/{self.info_manager.repo}/master/origin.list"
            )

        input_format = "plain"

        if self.info_manager.custom_pyfunceble_config:
            if (
                "adblock" in self.info_manager.custom_pyfunceble_config
                and self.info_manager.custom_pyfunceble_config["adblock"]
            ):
                input_format = "adblock"
            elif (
                "cli_decoding.adblock" in self.info_manager.custom_pyfunceble_config
                and self.info_manager.custom_pyfunceble_config["cli_decoding.adblock"]
            ):
                input_format = "adblock"

        return {
            "description": self.info_manager.platform_description,
            "url": url,
            "subject_type": "domain",
            "input_format": input_format,
            "link_type": "associated",
        }

    def search_matching_container(
        self, name: Optional[str] = None, shortname: Optional[str] = None
    ) -> Optional[dict]:
        """
        Queries the matching container.
        """

        search_info = {
            "approximate": False,
            "name": self.info_manager.name if not name else name,
            "shortname": self.info_manager.platform_shortname
            if not shortname
            else shortname,
        }

        params = {"limit": -1}

        req = self.session.post(
            f"{self.api_url}/v1/container/search", params=params, json=search_info
        )

        if req.status_code == 200:
            response = req.json()

            logging.debug(
                "Query-Matching-Container | URL: %s | Status Code: %s | "
                "Response:\n    %s",
                req.url,
                req.status_code,
                response,
            )

            return response

        logging.debug(
            "Query-Container | URL: %s | Status Code: %s | Response:\n    %s",
            req.url,
            req.status_code,
            req.json(),
        )

        return None

    def read_container(self):
        """
        Reads the container.
        """

        container_id = self.info_manager.platform_container_id

        req = self.session.get(f"{self.api_url}/v1/containers/{container_id}")

        if req.status_code == 200:
            response = req.json()

            logging.debug(
                "Read-Container | URL: %s | Status Code: %s | Response:\n    %s",
                req.url,
                req.status_code,
                response,
            )

            return response

        logging.debug(
            "Read-Container | URL: %s | Status Code: %s | Response:\n    %s",
            req.url,
            req.status_code,
            req.json(),
        )

        return None

    def read_remote_sources(self):
        """
        Reads the remote sources of the container.
        """

        container_id = self.info_manager.platform_container_id

        params = {"limit": -1}

        req = self.session.get(
            f"{self.api_url}/v1/containers/{container_id}/remote-sources",
            params=params,
        )

        if req.status_code == 200:
            response = req.json()

            logging.debug(
                "Read-Remote-Sources | URL: %s | Status Code: %s | Response:\n    %s",
                req.url,
                req.status_code,
                response,
            )

            return response

        if req.status_code == 204:
            logging.debug(
                "Read-Remote-Sources | URL: %s | Status Code: %s | NO CONTENT",
                req.url,
                req.status_code,
            )

            return []

        logging.debug(
            "Read-Remote-Sources | URL: %s | Status Code: %s | Response:\n    %s",
            req.url,
            req.status_code,
            req.json(),
        )

        return None

    def read_export_rules(self):
        """
        Reads the export rules of the container.
        """

        container_id = self.info_manager.platform_container_id

        params = {"limit": -1}

        req = self.session.get(
            f"{self.api_url}/v1/containers/{container_id}/export-rules",
            params=params,
        )

        if req.status_code == 200:
            response = req.json()

            logging.debug(
                "Read-Export-Rules | URL: %s | Status Code: %s | Response:\n    %s",
                req.url,
                req.status_code,
                response,
            )

            return response

        if req.status_code == 204:
            logging.debug(
                "Read-Export-Rules | URL: %s | Status Code: %s | NO CONTENT",
                req.url,
                req.status_code,
            )

            return []

        logging.debug(
            "Read-Export-Rules | URL: %s | Status Code: %s | Response:\n    %s",
            req.url,
            req.status_code,
            req.json(),
        )

        return []

    def download_export_rules(self, export_rule_id: str, destination: str):
        """
        Downloads the given export rule.

        :param export_rule_id:
            The ID of the export rule to download.

        :param destination:
            The destination of the downloaded file.
        """

        container_id = self.info_manager.platform_container_id

        logging.info(
            "Downloading export rule with ID: %s to %s",
            export_rule_id,
            destination,
        )

        req = self.session.get(
            f"{self.api_url}/v1/containers/{container_id}"
            f"/export-rules/{export_rule_id}/plain",
            stream=True,
        )

        if req.status_code == 200:
            with open(destination, "wb") as file_handler:
                for chunk in req.iter_content(chunk_size=1024):
                    file_handler.write(chunk)

            logging.info(
                "Successfully downloaded export rule with ID: %s to %s",
                export_rule_id,
                destination,
            )

            return True

        logging.critical(
            "Download-Export-Rule | URL: %s | Status Code: %s | Response:\n    %s",
            req.url,
            req.status_code,
            req.text,
        )

        return False

    def create_container(self):
        """
        Creates the container.
        """

        req = self.session.post(
            f"{self.api_url}/v1/containers", json=self.container_canonical_data
        )

        if req.status_code in (200, 202, 303):
            response = req.json()
            self.info_manager["platform_container_id"] = response["id"]

            logging.info(
                "Successfully created container with ID: %s",
                self.info_manager.platform_container_id,
            )
            logging.debug(
                "Create-Container | URL: %s | Status Code: %s | Response:\n    %s",
                req.url,
                req.status_code,
                response,
            )

            return response

        logging.critical(
            "Create-Container | URL: %s | Status Code: %s | Response:\n    %s",
            req.url,
            req.status_code,
            req.json(),
        )

        return req.json()

    def create_remote_source(self):
        """
        Creates the remote source.

        .. warning::
            This method assumes that only 1 remote source is desired.
        """

        container_id = self.info_manager.platform_container_id

        req = self.session.post(
            f"{self.api_url}/v1/containers/{container_id}/remote-sources",
            json=self.remote_source_canonical_data,
        )

        if req.status_code in (200, 202, 303):
            response = req.json()
            self.info_manager["platform_remote_source_id"] = response["id"]

            logging.info(
                "Successfully created remote source with ID: %s",
                response["id"],
            )

            logging.debug(
                "Create-Remote-Source | URL: %s | Status Code: %s | Response:\n    %s",
                req.url,
                req.status_code,
                response,
            )

            return response

        logging.critical(
            "Create-Remote-Source | URL: %s | Status Code: %s | Response:\n    %s",
            req.url,
            req.status_code,
            req.json(),
        )

        return req.json()

    def update_container(self):
        """
        Updates the container.
        """

        container_id = self.info_manager.platform_container_id

        req = self.session.patch(
            f"{self.api_url}/v1/containers/{container_id}",
            json=self.container_canonical_data,
        )

        if req.status_code in (200, 202, 303):
            response = req.json()
            self.info_manager["platform_container_id"] = response["id"]

            logging.info(
                "Successfully updated container with ID: %s",
                self.info_manager.platform_container_id,
            )

            logging.debug(
                "Update-Container | URL: %s | Status Code: %s | Response:\n    %s",
                req.url,
                req.status_code,
                response,
            )

            return req.json()

        logging.critical(
            "Update-Container | URL: %s | Status Code: %s | Response:\n    %s",
            req.url,
            req.status_code,
            req.json(),
        )

        return None

    def update_remote_source(self):
        """
        Updates the remote source.
        """

        container_id = self.info_manager.platform_container_id
        remote_source_id = self.info_manager.platform_remote_source_id

        req = self.session.patch(
            f"{self.api_url}/v1/containers/{container_id}"
            f"/remote-sources/{remote_source_id}",
            json=self.remote_source_canonical_data,
        )

        if req.status_code in (200, 202, 303):
            response = req.json()

            logging.info(
                "Successfully updated remote source with ID: %s",
                response["id"],
            )

            logging.debug(
                "Update-Remote-Source | URL: %s | Status Code: %s | Response:\n    %s",
                req.url,
                req.status_code,
                response,
            )

            return response

        logging.critical(
            "Update-Remote-Source | URL: %s | Status Code: %s | Response:\n    %s",
            req.url,
            req.status_code,
            req.json(),
        )

        return None

    def delete_container(self):
        """
        Deletes the container.

        :param container_id:
            The ID of the container to delete.

            .. note::
                If not given, we will follow the platform_container_id index.
        :type container_id: uuid.UUID
        """

        container_id = self.info_manager.platform_container_id

        req = self.session.delete(f"{self.api_url}/v1/containers/{container_id}")

        if req.status_code == 204:
            logging.info(
                "Successfully deleted container with ID: %s",
                container_id,
            )

            self.info_manager["platform_container_id"] = None
            self.info_manager["platform_remote_source_id"] = None

            return True

        logging.critical(
            "Delete-Container | URL: %s | Status Code: %s | Response:\n    %s",
            req.url,
            req.status_code,
            req.json(),
        )

        return False

    def delete_remote_source(self):
        """
        Deletes the remote source.
        """

        container_id = self.info_manager.platform_container_id
        remote_source_id = self.info_manager.platform_remote_source_id

        req = self.session.delete(
            f"{self.api_url}/v1/containers/{container_id}"
            f"/remote-sources/{remote_source_id}"
        )

        if req.status_code == 204:
            logging.info(
                "Successfully deleted remote source with ID: %s",
                remote_source_id,
            )

            self.info_manager["platform_remote_source_id"] = None

            return True

        logging.critical(
            "Delete-Remote-Source | URL: %s | Status Code: %s | Response:\n    %s",
            req.url,
            req.status_code,
            req.json(),
        )

        return False

    def upload(self):
        """
        Ensures that all locally defined information are uploaded to the platform
        - for testing.
        """

        if not self.info_manager.platform_container_id:
            found_containers = self.search_matching_container(
                name=self.info_manager.name,
                shortname=self.info_manager.platform_shortname,
            )

            if found_containers:
                self.info_manager["platform_container_id"] = found_containers[0]["id"]
                self.update_container()
            else:
                self.create_container()
        elif self.read_container():
            self.update_container()
        else:
            self.create_container()

        if not self.info_manager.platform_remote_source_id:
            found_remote_sources = self.read_remote_sources()

            if found_remote_sources:
                self.info_manager["platform_remote_source_id"] = found_remote_sources[
                    0
                ]["id"]
                self.update_remote_source()
            else:
                self.create_remote_source()
        else:
            dataset = self.read_remote_sources()

            if dataset:
                self.info_manager["platform_remote_source_id"] = dataset[0]["id"]

                self.update_remote_source()
            else:
                self.create_remote_source()

    def download(self):
        """
        Downloads the latest compiled version of the dataset.
        """

        if not self.info_manager.platform_container_id:
            found_containers = self.search_matching_container(
                name=self.info_manager.name,
                shortname=self.info_manager.platform_shortname,
            )

            if found_containers:
                self.info_manager["platform_container_id"] = found_containers[0]["id"]

        if not self.info_manager.platform_container_id:
            return False

        wanted_export_rules = []

        expected_availability_status = {
            "active": True,
            "inactive": False,
            "invalid": False,
        }
        expected_reputation_status = {
            "sane": False,
            "malicious": False,
            "invalid": False,
        }
        expected_syntax_status = {
            "valid": False,
            "invalid": False,
        }

        for export_rule in self.read_export_rules():
            if (
                all(
                    y == export_rule["availability"][x]
                    for x, y in expected_availability_status.items()
                )
                and all(
                    y == export_rule["reputation"][x]
                    for x, y in expected_reputation_status.items()
                )
                and all(
                    y == export_rule["syntax"][x]
                    for x, y in expected_syntax_status.items()
                )
            ):
                wanted_export_rules.append(export_rule)

        files = []

        for export_rule in wanted_export_rules:
            logging.debug("Downloading export rule: %r", export_rule)

            with tempfile.NamedTemporaryFile(
                delete=False, suffix="_export_rule"
            ) as tmp_filestream:
                if not self.download_export_rules(
                    export_rule["id"], tmp_filestream.name
                ):
                    continue

                tmp_filestream.seek(0)
                files.append(tmp_filestream.name)

        logging.info("Starting to merge the downloaded files.")

        # pylint: disable=consider-using-with
        temp_output_file = tempfile.NamedTemporaryFile(
            mode="w", delete=False, suffix="_output"
        )

        output_file = FileHelper(
            os.path.join(
                self.info_manager.WORKSPACE_DIR,
                dead_hosts.launcher.defaults.paths.OUTPUT_FILENAME,
            )
        )

        temp_output_file.write(
            "\n".join(dead_hosts.launcher.defaults.paths.OUTPUT_FILE_HEADER) + "\n\n"
        )

        written = False

        for file in files:
            file = FileHelper(file)

            with file.open("r", encoding="utf-8") as file_stream:
                for line in file_stream:
                    if line.startswith("#"):
                        continue

                    temp_output_file.write(line)
                    written = True

        temp_output_file.seek(0)

        logging.info("Finished to merge the downloaded files.")

        if written:
            logging.info("Moving the merged file to its final destination.")
            FileHelper(temp_output_file.name).move(output_file.path)
            logging.info("Moved the merged file to its final destination.")

        logging.info("Cleaning up temporary files.")
        for file in files:
            os.remove(file)
        logging.info("Cleaned up temporary files.")

        return True
