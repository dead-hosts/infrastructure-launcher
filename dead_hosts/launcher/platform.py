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
    DEFAULT_SCOPE = "example-username"

    _api_url = DEFAULT_API_URL
    _scope = DEFAULT_SCOPE
    __cached_header: dict = {}

    info_manager: InfoManager
    headers: dict = {}
    session: requests.Session

    def __init__(self, info_manager: InfoManager) -> None:
        self.info_manager = info_manager

        self.api_url = EnvironmentVariableHelper("DEV_PLATFORM_API_URL").get_value(
            default=None
        ) or EnvironmentVariableHelper("PLATFORM_API_URL").get_value(
            default=self.DEFAULT_API_URL
        )

        api_token = EnvironmentVariableHelper("DEV_PLATFORM_API_TOKEN").get_value(
            default=None
        ) or EnvironmentVariableHelper("PLATFORM_API_TOKEN").get_value(default=None)

        self.scope = EnvironmentVariableHelper("DEV_PLATFORM_SCOPE").get_value(
            default=None
        ) or EnvironmentVariableHelper("PLATFORM_SCOPE").get_value(
            default=self.DEFAULT_SCOPE
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
    def scope(self) -> str:
        """
        Provides the scope to use.
        """

        return self._scope

    @scope.setter
    def scope(self, value: str) -> None:
        """
        Sets the scope to use.
        """

        self._scope = value

    @property
    def container_id(self) -> str:
        """
        Provides the container ID to use.
        """

        return self.info_manager.platform_container_id

    @container_id.setter
    def container_id(self, value: str) -> None:
        """
        Sets the container ID to use.
        """

        self.info_manager["platform_container_id"] = value

    @property
    def container_canonical_name(self) -> str:
        """
        Provides the container name to use.
        """

        return self.info_manager.platform_container_name

    @container_canonical_name.setter
    def container_canonical_name(self, value: str) -> None:
        """
        Sets the container name to use.
        """

        self.info_manager["platform_container_name"] = value

    @property
    def container_description(self) -> str:
        """
        Provides the container description to use.
        """

        return self.info_manager.platform_description

    @container_description.setter
    def container_description(self, value: str) -> None:
        """
        Sets the container description to use.
        """

        self.info_manager["platform_description"] = value

    @property
    def remote_source_id(self) -> str:
        """
        Provides the remote source ID to use.
        """

        return self.info_manager.platform_remote_source_id

    @remote_source_id.setter
    def remote_source_id(self, value: str) -> None:
        """
        Sets the remote source ID to use.
        """

        self.info_manager["platform_remote_source_id"] = value

    @property
    def container_display_name(self) -> str:
        """
        Provides the container display name to use.
        """

        return self.info_manager.name

    @property
    def container_slug(self) -> str:
        """
        Provides the container slug to use.
        """

        return f"{self.scope}/{self.info_manager.platform_container_name}"

    @property
    def container_canonical_data(self) -> dict:
        """
        Provides the canonical data of the container.
        """

        return {
            "availability_test": True,
            "reputation_test": False,
            "syntax_test": True,
            "name": self.container_canonical_name,
            "display_name": self.container_canonical_name,
            "description": self.container_description,
            "public": False,
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
            "description": self.container_description,
            "url": url,
            "subject_type": "domain",
            "input_format": input_format,
            "link_type": "associated",
        }

    def search_matching_container(
        self, display_name: Optional[str] = None, name: Optional[str] = None
    ) -> Optional[dict]:
        """
        Queries the matching container.
        """

        logging.info(
            "Searching for container matching name (%s) or display name (%s).",
            self.container_display_name if not display_name else display_name,
            self.container_canonical_name if not name else name,
        )

        search_info = {
            "approximate": False,
            "display_name": (
                self.container_display_name if not display_name else display_name
            ),
            "name": (self.container_canonical_name if not name else name),
            "username": self.scope,
        }

        params = {"limit": -1}

        try:
            req = self.session.post(
                f"{self.api_url}/v1/containers/search", params=params, json=search_info
            )
        except requests.exceptions.RequestException:
            logging.critical("Failed to communicate with platform. Opt-Out forgotten?")
            return None

        if req.status_code == 200:
            response = req.json()

            logging.debug(
                "Query-Matching-Container | URL: %s | Status Code: %s | "
                "Response:\n    %s",
                req.url,
                req.status_code,
                response,
            )

            logging.info(
                "Found %d matching containers.",
                len(response),
            )

            return response

        logging.debug(
            "Query-Container | URL: %s | Status Code: %s | Response:\n    %s",
            req.url,
            req.status_code,
            req.text,
        )

        logging.info("Found no matching container.")

        return None

    def read_container(self):
        """
        Reads the container.
        """

        logging.info("Reading container matching name (%s).", self.container_slug)

        try:
            req: requests.Response = self.session.get(
                f"{self.api_url}/v1/containers/{self.container_slug}"
            )
        except requests.exceptions.RequestException:
            logging.critical("Failed to communicate with platform. Opt-Out forgotten?")
            return None

        if req.status_code == 200:
            response = req.json()

            logging.debug(
                "Read-Container | URL: %s | Status Code: %s | Response:\n    %s",
                req.url,
                req.status_code,
                response,
            )

            logging.info("Found container matching name (%s).", self.container_slug)

            return response

        logging.debug(
            "Read-Container | URL: %s | Status Code: %s | Response:\n    %s",
            req.url,
            req.status_code,
            req.text,
        )

        logging.info("Found no container matching name (%s).", self.container_slug)

        return None

    def read_remote_sources(self):
        """
        Reads the remote sources of the container.
        """

        logging.info(
            "Reading remote sources of container matching name (%s).",
            self.container_slug,
        )

        params = {"limit": -1}

        try:
            req = self.session.get(
                f"{self.api_url}/v1/containers/{self.container_slug}/remote-sources",
                params=params,
            )
        except requests.exceptions.RequestException:
            logging.critical("Failed to communicate with platform. Opt-Out forgotten?")
            return []

        if req.status_code == 200:
            response = req.json()

            logging.debug(
                "Read-Remote-Sources | URL: %s | Status Code: %s | Response:\n    %s",
                req.url,
                req.status_code,
                response,
            )

            logging.info(
                "Found %d remote sources of container matching name (%s).",
                len(response),
                self.container_slug,
            )

            return response

        if req.status_code == 204:
            logging.debug(
                "Read-Remote-Sources | URL: %s | Status Code: %s | NO CONTENT",
                req.url,
                req.status_code,
            )

            logging.info(
                "Found no remote sources of container  matching name (%s).",
                self.container_slug,
            )

            return []

        logging.debug(
            "Read-Remote-Sources | URL: %s | Status Code: %s | Response:\n    %s",
            req.url,
            req.status_code,
            req.text,
        )

        logging.info(
            "Found no remote sources of container matching name (%s).",
            self.container_slug,
        )

        return []

    def read_export_rules(self):
        """
        Reads the export rules of the container.
        """

        logging.info(
            "Reading export rules of container matching name (%s).",
            self.container_slug,
        )

        params = {"limit": -1}

        try:
            req = self.session.get(
                f"{self.api_url}/v1/containers/{self.container_slug}/export-rules",
                params=params,
            )
        except requests.exceptions.RequestException:
            logging.critical("Failed to communicate with platform. Opt-Out forgotten?")
            return []

        if req.status_code == 200:
            response = req.json()

            logging.debug(
                "Read-Export-Rules | URL: %s | Status Code: %s | Response:\n    %s",
                req.url,
                req.status_code,
                response,
            )

            logging.info(
                "Found %d export rules of container matching name (%s).",
                len(response),
                self.container_slug,
            )

            return response

        if req.status_code == 204:
            logging.debug(
                "Read-Export-Rules | URL: %s | Status Code: %s | NO CONTENT",
                req.url,
                req.status_code,
            )

            logging.info(
                "Found no export rules of container matching name (%s).",
                self.container_slug,
            )

            return []

        logging.debug(
            "Read-Export-Rules | URL: %s | Status Code: %s | Response:\n    %s",
            req.url,
            req.status_code,
            req.text,
        )

        logging.info(
            "Found no export rules of container matching name (%s).",
            self.container_slug,
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

        logging.info(
            "Downloading export rule with ID: %s to %s",
            export_rule_id,
            destination,
        )

        try:
            req = self.session.get(
                f"{self.api_url}/v1/containers/{self.container_slug}"
                f"/export-rules/{export_rule_id}/plain",
                stream=True,
            )
        except requests.exceptions.RequestException:
            logging.critical("Failed to communicate with platform. Opt-Out forgotten?")
            return False

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

        if req.status_code == 204:
            logging.info(
                "Export rule (%s) is empty.",
                export_rule_id,
            )

            return False

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

        logging.info("Creating container.")

        try:
            req = self.session.post(
                f"{self.api_url}/v1/containers", json=self.container_canonical_data
            )
        except requests.exceptions.RequestException:
            logging.critical("Failed to communicate with platform. Opt-Out forgotten?")
            return ""

        if req.status_code in (200, 202, 303):
            response = req.json()

            self.container_id = response["id"]
            self.container_canonical_name = response["name"]

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
            req.text,
        )

        logging.info("Failed to create container.")

        try:
            return req.json()
        except json.JSONDecodeError:
            return req.text

    def create_remote_source(self):
        """
        Creates the remote source.

        .. warning::
            This method assumes that only 1 remote source is desired.
        """

        logging.info(
            "Creating remote source for container matching name (%s)",
            self.container_slug,
        )

        try:
            req = self.session.post(
                f"{self.api_url}/v1/containers/{self.container_slug}/remote-sources",
                json=self.remote_source_canonical_data,
            )
        except requests.exceptions.RequestException:
            logging.critical("Failed to communicate with platform. Opt-Out forgotten?")
            return ""

        if req.status_code in (200, 202, 303):
            response = req.json()

            self.remote_source_id = response["id"]

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
            req.text,
        )

        logging.info(
            "Failed to create remote source for container matching name (%s)",
            self.container_slug,
        )

        try:
            return req.json()
        except json.JSONDecodeError:
            return req.text

    def update_container(self):
        """
        Updates the container.
        """

        logging.info(
            "Updating container matching name (%s)",
            self.container_slug,
        )

        try:
            req = self.session.patch(
                f"{self.api_url}/v1/containers/{self.container_slug}",
                json=self.container_canonical_data,
            )
        except requests.exceptions.RequestException:
            logging.critical("Failed to communicate with platform. Opt-Out forgotten?")
            return ""

        if req.status_code in (200, 202, 303):
            response = req.json()

            self.container_id = response["id"]
            self.container_canonical_name = response["name"]

            logging.info(
                "Successfully updated container matching name (%s)",
                self.container_slug,
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
            req.text,
        )

        logging.info(
            "Failed to update container matching name (%s)",
            self.container_slug,
        )

        try:
            return req.json()
        except json.JSONDecodeError:
            return req.text

    def update_remote_source(self):
        """
        Updates the remote source.
        """

        logging.info(
            "Updating remote source with ID (%s) for container matching name (%s)",
            self.remote_source_id,
            self.container_slug,
        )

        try:
            req = self.session.patch(
                f"{self.api_url}/v1/containers/{self.container_slug}"
                f"/remote-sources/{self.remote_source_id}",
                json=self.remote_source_canonical_data,
            )
        except requests.exceptions.RequestException:
            logging.critical("Failed to communicate with platform. Opt-Out forgotten?")
            return ""

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
            req.text,
        )

        logging.info(
            "Failed to update remote source with ID (%s) for container matching "
            "name (%s)",
            self.remote_source_id,
            self.container_slug,
        )

        try:
            return req.json()
        except json.JSONDecodeError:
            return req.text

    def delete_container(self):
        """
        Deletes the container.

        :param container_id:
            The ID of the container to delete.

            .. note::
                If not given, we will follow the platform_container_id index.
        :type container_id: uuid.UUID
        """

        logging.info(
            "Deleting container matching name (%s).",
            self.container_slug,
        )

        try:
            req = self.session.delete(
                f"{self.api_url}/v1/containers/{self.container_slug}"
            )
        except requests.exceptions.RequestException:
            logging.critical("Failed to communicate with platform. Opt-Out forgotten?")
            return False

        if req.status_code == 204:
            logging.info(
                "Successfully deleted container matching name (%s).",
                self.container_slug,
            )

            self.container_id = None
            self.remote_source_id = None

            return True

        logging.critical(
            "Delete-Container | URL: %s | Status Code: %s | Response:\n    %s",
            req.url,
            req.status_code,
            req.text,
        )

        logging.info(
            "Failed to delete container matching name (%s).",
            self.container_slug,
        )

        return False

    def delete_remote_source(self):
        """
        Deletes the remote source.
        """

        logging.info(
            "Deleting remote source with ID (%s) for container matching name (%s)",
            self.remote_source_id,
            self.container_slug,
        )

        try:
            req = self.session.delete(
                f"{self.api_url}/v1/containers/{self.container_slug}"
                f"/remote-sources/{self.remote_source_id}"
            )
        except requests.exceptions.RequestException:
            logging.critical("Failed to communicate with platform. Opt-Out forgotten?")
            return False

        if req.status_code == 204:
            logging.info(
                "Successfully deleted remote source with ID: %s",
                self.remote_source_id,
            )

            self.remote_source_id = None

            return True

        logging.critical(
            "Delete-Remote-Source | URL: %s | Status Code: %s | Response:\n    %s",
            req.url,
            req.status_code,
            req.text,
        )

        logging.info(
            "Failed to delete remote source with ID (%s) for container matching "
            "name (%s)",
            self.remote_source_id,
            self.container_slug,
        )

        return False

    def upload(self):
        """
        Ensures that all locally defined information are uploaded to the platform
        - for testing.
        """

        if not self.container_id:
            found_containers = self.search_matching_container()

            if found_containers:
                self.container_id = found_containers[0]["id"]
                self.container_canonical_name = found_containers[0]["name"]

                self.update_container()
            else:
                self.create_container()
        elif self.read_container():
            self.update_container()
        else:
            self.create_container()

        if not self.remote_source_id:
            found_remote_sources = self.read_remote_sources()

            if found_remote_sources:
                self.remote_source_id = found_remote_sources[0]["id"]
                self.update_remote_source()
            else:
                self.create_remote_source()
        else:
            dataset = self.read_remote_sources()

            if dataset:
                self.remote_source_id = dataset[0]["id"]

                self.update_remote_source()
            else:
                self.create_remote_source()

    def download(self):
        """
        Downloads the latest compiled version of the dataset.
        """

        if not self.container_id:
            found_containers = self.search_matching_container()

            if found_containers:
                self.container_id = found_containers[0]["id"]
                self.container_canonical_name = found_containers[0]["name"]

        if not self.container_id:
            logging.info("No container found. Aborting.")
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
