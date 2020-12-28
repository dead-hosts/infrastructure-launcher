"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides our default Travis CI settings.

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

import os
from typing import Optional

from PyFunceble.helpers.environment_variable import EnvironmentVariableHelper

env_var = EnvironmentVariableHelper()

DEFAULT_EMAIL: str = "dead-hosts@outlook.com"

if env_var.set_name("TRAVIS_BUILD_DIR").exists():
    BUILD_DIR: Optional[str] = env_var.get_value()
else:
    BUILD_DIR: Optional[str] = os.getcwd()

if env_var.set_name("GH_TOKEN").exists():
    GITHUB_TOKEN: Optional[str] = env_var.get_value()
else:
    GITHUB_TOKEN: Optional[str] = None

if env_var.set_name("GIT_EMAIL").exists():
    GIT_EMAIL: Optional[str] = env_var.get_value()
else:
    GIT_EMAIL: Optional[str] = None

if env_var.set_name("GIT_BRANCH").exists():
    GIT_BRANCH: str = env_var.get_value()
else:
    GIT_BRANCH: str = "master"

if env_var.set_name("GIT_DISTRIBUTION_BRANCH").exists():
    GIT_DISTRIBUTION_BRANCH: str = env_var.get_value()
else:
    GIT_DISTRIBUTION_BRANCH: str = GIT_BRANCH

if env_var.set_name("NO_CI_CONFIG_UPDATE").exists():
    UPDATE_CI_CONFIG: bool = False
else:
    UPDATE_CI_CONFIG: bool = True

UNIFIED_CONFIG: dict = {
    "env": {"matrix": ['PYTHON_VERSION="3.8.0"']},
    "language": "generic",
    "os": ["linux"],
    "dist": "bionic",
    "addons": {"apt": {"packages": ["dos2unix"]}},
    "install": [
        'export PATH="${HOME}/miniconda/bin:${PATH}"',
        # pylint: disable=line-too-long
        "wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh",
        "bash miniconda.sh -b -p ${HOME}/miniconda",
        "hash -r",
        "conda config --set always_yes yes --set changeps1 no",
        "conda update -q conda",
        'conda create -q -n launcher-environment python="${PYTHON_VERSION}"',
        "source activate launcher-environment",
        "python -VV",
        "pip --version",
        "pip install --upgrade dead-hosts-launcher",
        "rm miniconda.sh",
    ],
    "script": ["dead_hosts_launcher --version", "dead_hosts_launcher"],
    "notifications": {
        "email": {
            "recipients": ["dead-hosts@outlook.com"],
            "on_success": "change",
            "on_failure": "always",
        }
    },
}
