"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the updater of the README file.

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

import importlib.resources
import logging
import os

from PyFunceble.helpers.file import FileHelper
from PyFunceble.helpers.regex import RegexHelper

import dead_hosts.launcher.defaults.markers
import dead_hosts.launcher.defaults.paths
import dead_hosts.launcher.defaults.travis_ci
from dead_hosts.launcher.updater.base import UpdaterBase


class ReadmeUpdater(UpdaterBase):
    """
    Provides the updater of the README file.
    """

    DESTINATION: FileHelper = FileHelper(
        os.path.join(
            dead_hosts.launcher.defaults.travis_ci.BUILD_DIR,
            dead_hosts.launcher.defaults.paths.README_FILENAME,
        )
    )

    @property
    def authorized(self) -> bool:
        return self.DESTINATION.exists()

    def pre(self) -> "ReadmeUpdater":
        logging.info("Started to update the content of %r!", self.DESTINATION.path)

        return self

    def post(self) -> "ReadmeUpdater":
        logging.info("Finished to update the content of %r!", self.DESTINATION.path)

        return self

    def start(self) -> "ReadmeUpdater":
        logging.info(
            "Started to update the `About PyFunceble` section of %r",
            self.DESTINATION.path,
        )

        with importlib.resources.path(
            "dead_hosts.launcher.data.docs", "about_pyfunceble.md"
        ) as file_path:
            updated_version = RegexHelper(
                dead_hosts.launcher.defaults.markers.ABOUT_FUNCEBLE_REGEX
            ).replace_match(self.DESTINATION.read(), FileHelper(file_path).read())

        logging.info(
            "Finished to update the `About PyFunceble` section of %r",
            self.DESTINATION.path,
        )

        logging.info(
            "Started to update the `About Dead-Hosts` section of %r",
            self.DESTINATION.path,
        )

        with importlib.resources.path(
            "dead_hosts.launcher.data.docs", "about_dead_hosts.md"
        ) as file_path:
            updated_version = RegexHelper(
                dead_hosts.launcher.defaults.markers.ABOUT_DEAD_HOSTS_REGEX
            ).replace_match(self.DESTINATION.read(), FileHelper(file_path).read())

        logging.info(
            "Finished to update the `About Dead-Hosts` section of %s",
            self.DESTINATION.path,
        )

        self.DESTINATION.write(updated_version, overwrite=True)

        return self
