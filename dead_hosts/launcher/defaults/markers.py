"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides our default markers.

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

LAUNCH_TEST: str = r"Launch\stest"
DATE_FORMAT: str = "%Y-%m-%dT%H:%M:%S%z"
ABOUT_FUNCEBLE_REGEX: str = r"(?s)#\s+About\sPyFunceble(.*)"
ABOUT_DEAD_HOSTS_REGEX: str = r"(?s)#\s+About\sDead-[hH]osts.+?(?=-{4,})"
MAINTENANCE_COMMIT_MESSAGE: str = "[SELF][Maintenance]"
