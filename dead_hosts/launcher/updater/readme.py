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

import logging

import PyFunceble.helpers as pyfunceble_helpers

from ..configuration import Markers, Paths
from .base import Base


class ReadMeUpdater(Base):
    """
    Provides the updater of the README file.
    """

    def __init__(self) -> None:
        self.destination = pyfunceble_helpers.File(Paths.readme_filename)

        super().__init__()

    def authorization(self) -> bool:
        return self.destination.exists()

    def pre(self):
        logging.info("Started to update the content of %s!", self.destination.path)

    def post(self):
        logging.info("Finished to update the content of %s!", self.destination.path)

    def start(self) -> None:
        logging.info(
            "Started to update the `About PyFunceble` section of %s",
            self.destination.path,
        )

        updated_version = pyfunceble_helpers.Regex(
            Markers.extract_about_pyfunceble
        ).replace_match(self.destination.read(), Markers.about_pyfunceble)

        logging.info(
            "Finished to update the `About PyFunceble` section of %s",
            self.destination.path,
        )

        logging.info(
            "Started to update the `About Dead-Hosts` section of %s",
            self.destination.path,
        )

        updated_version = pyfunceble_helpers.Regex(
            Markers.extract_about_dead_hosts
        ).replace_match(self.destination.read(), Markers.about_dead_hosts)

        logging.info(
            "Finished to update the `About Dead-Hosts` section of %s",
            self.destination.path,
        )

        self.destination.write(updated_version, overwrite=True)
