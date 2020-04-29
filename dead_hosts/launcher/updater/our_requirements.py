"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the updater of our requirements.txt file.

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
from typing import Optional

import PyFunceble.helpers as pyfunceble_helpers

from ..configuration import Links
from .base import Base


class OurRequirementsUpdater(Base):
    """
    Provides the updater of our requirements.txt file.
    """

    destination: Optional[pyfunceble_helpers.File] = None

    def authorization(self) -> bool:
        return not pyfunceble_helpers.File("info.example.json").exists()

    def pre(self):
        self.destination = pyfunceble_helpers.File(
            self.working_dir + Links.our_requirements["destination"]
        )

        logging.info("Started to update %s", self.destination.path)

    def post(self):
        logging.info("Finished to update %s", self.destination.path)

    def start(self):
        pyfunceble_helpers.Download(Links.our_requirements["link"]).text(
            destination=self.destination.path
        )
