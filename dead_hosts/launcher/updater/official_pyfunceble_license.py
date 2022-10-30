"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the updater of the official pyfunceble LICENSE.

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

import dead_hosts.launcher.defaults.links
from dead_hosts.launcher.info_manager import InfoManager
from dead_hosts.launcher.updater.base import UpdaterBase


class OfficialPyFuncebleLicenseUpdater(UpdaterBase):
    """
    Provides the updater of the official PyFunceble license file.
    """

    def __init__(self, info_manager: InfoManager) -> None:
        self.destination = os.path.join(
            info_manager.WORKSPACE_DIR,
            dead_hosts.launcher.defaults.links.OFFICIAL_PYFUNCEBLE_LICENSE[
                "destination"
            ],
        )
        super().__init__(info_manager)

    @property
    def authorized(self) -> bool:
        return True

    def pre(self) -> "OfficialPyFuncebleLicenseUpdater":
        logging.info("Started to update %r", self.destination)

        return self

    def post(self) -> "OfficialPyFuncebleLicenseUpdater":
        logging.info("Finished to update %s", self.destination)

        return self

    def start(self) -> "OfficialPyFuncebleLicenseUpdater":
        DownloadHelper(
            dead_hosts.launcher.defaults.links.OFFICIAL_PYFUNCEBLE_LICENSE["link"]
        ).download_text(destination=self.destination)

        return self
