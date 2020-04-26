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

import PyFunceble.helpers as pyfunceble_helpers

from ..configuration import Links
from .cross_pyfunceble_config import CrossPyFuncebleConfigUpdater


class PyFuncebleConfigUpdater(CrossPyFuncebleConfigUpdater):
    """
    Provides the updater of the PyFunceble configuration.
    """

    def authorization(self) -> bool:
        return (
            not self.cross_pyfunceble_config_file.exists()
            and not self.info_manager.own_management
        )

    def pre(self) -> None:
        logging.info(
            "Started to update %s.", self.pyfunceble_config_file.path,
        )

    def post(self) -> None:
        logging.info(
            "Finished to update %s.", self.pyfunceble_config_file.path,
        )

    def start(self) -> None:
        crossed_version = pyfunceble_helpers.Download(
            Links.cross_pyfunceble_configuration["link"]
        ).text()

        local_version = pyfunceble_helpers.Dict.from_yaml(crossed_version)

        if self.info_manager.ping:
            logging.info("Ping names given, appending them to the commit message.")

            local_version["ci_autosave_final_commit"] = self.get_commit_message(
                pings=self.info_manager.get_ping_for_commit()
            )

        if self.info_manager.custom_pyfunceble_config and isinstance(
            self.info_manager.custom_pyfunceble_config, dict
        ):
            logging.info(
                "Custom PyFunceble configuration given, "
                "appending them to the local configuration file."
            )

            local_version = pyfunceble_helpers.Merge(
                self.info_manager.custom_pyfunceble_config
            ).into(local_version, strict=True)

        logging.debug("Interpreted PyFunceble config:\n%s", local_version)

        pyfunceble_helpers.Dict(local_version).to_yaml_file(
            self.pyfunceble_config_file.path
        )
