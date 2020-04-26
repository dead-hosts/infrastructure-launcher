"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the updaters.

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

from .cross_pyfunceble_config import CrossPyFuncebleConfigUpdater
from .official_pyfunceble_config import OfficialPyFuncebleConfigUpdater
from .official_pyfunceble_license import OfficialPyFuncebleLicenseUpdater
from .our_license import OurLicenseUpdater
from .our_requirements import OurRequirementsUpdater
from .pyfunceble_config import PyFuncebleConfigUpdater
from .readme import ReadMeUpdater
from .travis_ci_config import TravisCIConfigUpdater


def exec_all() -> None:
    """
    Executes all updater.
    """

    CrossPyFuncebleConfigUpdater()
    PyFuncebleConfigUpdater()
    OfficialPyFuncebleConfigUpdater()
    OfficialPyFuncebleLicenseUpdater()

    ReadMeUpdater()
    OurLicenseUpdater()
    OurRequirementsUpdater()

    TravisCIConfigUpdater()
