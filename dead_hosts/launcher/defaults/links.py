"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides our default links.

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

# pylint: disable=line-too-long

OUR_LICENSE: dict = {
    "link": "https://raw.githubusercontent.com/dead-hosts/repository-structure/master/LICENSE",
    "destination": "LICENSE",
}

OUR_REQUIREMENTS: dict = {
    "link": "https://raw.githubusercontent.com/dead-hosts/repository-structure/master/requirements.txt",
    "destination": "requirements.txt",
}

OFFICIAL_PYFUNCEBLE_LICENSE: dict = {
    "link": "https://raw.githubusercontent.com/funilrys/PyFunceble/dev/LICENSE",
    "destination": "LICENSE_PyFunceble",
}

OFFICIAL_PYFUNCEBLE_CONFIG: dict = {
    "link": "https://raw.githubusercontent.com/funilrys/PyFunceble/dev/PyFunceble/data/infrastructure/.PyFunceble_production.yaml",
    "destination": ".PyFunceble_production.yaml",
}

GHA_MAIN_WORKFLOW: dict = {
    "link": "https://github.com/dead-hosts/template/raw/master/.github/workflows/main.yml",
    "destination": "main.yml",
}


GHA_SCHEDULER_WORKFLOW: dict = {
    "link": "https://github.com/dead-hosts/template/raw/master/.github/workflows/scheduler.yml",
    "destination": "scheduler.yml",
}
