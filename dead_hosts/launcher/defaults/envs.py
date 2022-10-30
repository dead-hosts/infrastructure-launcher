"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides our environment related defaults.

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

import os
from typing import List, Optional

from PyFunceble.helpers.environment_variable import EnvironmentVariableHelper

env_var = EnvironmentVariableHelper()

DEFAULT_EMAIL: str = "dead-hosts@outlook.com"

UNDER_CI_ENVS: List[str] = ["GITHUB_ACTIONS"]
UNDER_CI: bool = any(env_var.set_name(x).exists() for x in UNDER_CI_ENVS)

WORKSPACE_DIR: Optional[str] = env_var.set_name("GITHUB_WORKSPACE").get_value(
    default=os.getcwd()
)

GITHUB_TOKEN: Optional[str] = env_var.set_name("GITHUB_TOKEN").get_value(default=None)
GIT_EMAIL: Optional[str] = env_var.set_name("GIT_EMAIL").get_value(default=None)
GIT_NAME: str = env_var.set_name("GIT_NAME").get_value(default="dead-hostsbot")
GIT_BRANCH: str = env_var.set_name("GIT_BRANCH").get_value(default="master")
GIT_DISTRIBUTION_BRANCH: str = env_var.set_name("GIT_DISTRIBUTION_BRANCH").get_value(
    default=GIT_BRANCH
)
