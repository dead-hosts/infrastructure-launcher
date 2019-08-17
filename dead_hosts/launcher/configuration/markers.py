"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides a mix of a bit of everything which can't be structured.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Project link:
    https://github.com/dead-hosts/infrastructure-launcher

License:
::

    MIT License

    Copyright (c) 2019 Dead Hosts
    Copyright (c) 2019 Nissar Chababy

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


class Markers:
    """
    Provides some markers.
    """

    launch_test = r"Launch\stest"
    """
    Set the marker to use as a regex in order to match a test launch
    (from the beginning) request.
    """

    default_datetime_format = "%Y-%m-%dT%H:%M:%S%z"
    """
    Set the default date time format.
    """

    extract_about_pyfunceble = r"(?s)#\s+About\sPyFunceble(.*)"
    """
    Set the regex to use to extract the PyFunceble description.
    """

    extract_about_dead_hosts = r"(?s)#\s+About\sDead-[hH]osts.+?(?=-{4,})"
    """
    Set the regex to use to extract the dead-hosts description-
    """

    about_pyfunceble = """# About PyFunceble

PyFunceble is the tool that our infrastructure use to get the status (ACTIVE, INVALID, INACTIVE) of a given domain or IPv4.

Please find more information about it there:

* http://pyfunceble.github.io
* http://pyfunceble.readthedocs.io
* https://github.com/funilrys/PyFunceble

"""
    """
    Provides the information about PyFunceble.
    """

    about_dead_hosts = """# About Dead-hosts

[Dead-Hosts](https://github.com/dead-hosts) is the replacement of the original idea behind [funilrys/dead-hosts](https://github.com/funilrys/dead-hosts).
Indeed, the idea was to test - with the help of PyFunceble and Travis CI - hosts file, list of domains or even bocklist to have a list of only active domains or IP.

Today, we provide our infrastructure for anybody who want it. [Just ask](https://github.com/dead-hosts/dev-center/issues/new?template=inclusion-request.md)!

"""

    maintenance_commit_message = "[SELF][Maintenance]"
    """
    Set the commit message to use when we commit/do some maintenance commits.
    """
