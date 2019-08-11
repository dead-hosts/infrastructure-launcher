"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the differnt links we have to natively interact with.

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


class Links:
    """
    Provides some links.
    """

    # pylint: disable=line-too-long

    our_license = {
        "link": "https://raw.githubusercontent.com/dead-hosts/repository-structure/master/LICENSE",
        "destination": "LICENSE",
    }
    """
    Set the link of our shared license.
    """

    cross_pyfunceble_configuration = {
        "link": "https://raw.githubusercontent.com/dead-hosts/repository-structure/master/.PyFunceble_cross_repositories_config.yaml",
        "destination": ".PyFunceble.yaml",
    }
    """
    Set the link to our cross repository's PyFunceble configuration.
    """

    pyfunceble_official_config = {
        "link": "https://raw.githubusercontent.com/funilrys/PyFunceble/dev/.PyFunceble_production.yaml",
        "destination": ".PyFunceble_production.yaml",
    }
    """
    Set the link to the official pyfunceble configuration to use.
    """

    pyfunceble_official_license = {
        "link": "https://raw.githubusercontent.com/funilrys/PyFunceble/dev/LICENSE",
        "destination": "LICENSE_PyFunceble",
    }
    """
    Set the link to the official pyfunceble configuration to use.
    """
