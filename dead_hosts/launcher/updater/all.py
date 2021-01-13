"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides all the updater in one place.

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

from dead_hosts.launcher.info_manager import InfoManager
from dead_hosts.launcher.updater.github_actions_workflows import GHAWorkflowsUpdater
from dead_hosts.launcher.updater.official_pyfunceble_config import (
    OfficialPyFuncebleConfigUpdater,
)
from dead_hosts.launcher.updater.official_pyfunceble_license import (
    OfficialPyFuncebleLicenseUpdater,
)
from dead_hosts.launcher.updater.our_infrastructure import OurInfrastructureUpdater
from dead_hosts.launcher.updater.our_license import OurLicenseUpdater
from dead_hosts.launcher.updater.our_requirements import OurRequirementsUpdater
from dead_hosts.launcher.updater.pyfunceble_config import PyFuncebleConfigUpdater
from dead_hosts.launcher.updater.pyfunceble_config_location import (
    PyFuncebleConfigLocationUpdater,
)
from dead_hosts.launcher.updater.readme import ReadmeUpdater


def execute_all_updater(info_manager: InfoManager) -> None:
    """
    Executes all updated in a logical order.
    """

    OurInfrastructureUpdater(info_manager)
    PyFuncebleConfigLocationUpdater(info_manager)
    GHAWorkflowsUpdater(info_manager)

    PyFuncebleConfigUpdater(info_manager)
    OfficialPyFuncebleConfigUpdater(info_manager)
    OfficialPyFuncebleLicenseUpdater(info_manager)

    ReadmeUpdater(info_manager)
    OurLicenseUpdater(info_manager)
    OurRequirementsUpdater(info_manager)
