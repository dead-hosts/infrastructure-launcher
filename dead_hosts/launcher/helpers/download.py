"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides a way to download things.

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

import requests

from .file import File


class Download:
    """
    Provides an interface for file download.

    :param str link: The link to download.
    """

    def __init__(self, link):
        self.link = link

    def text(self, destination=False, success_status_code=None):
        """
        Downloads the text of the given link.

        :param str destination:
            Where we are supposed to write the downloaded content.

            .. note::
                If a non :code:`str` value is given, we don't save into a file.
        :param list success_status_code: The list of HTTP status code to consider as success.
        """

        if not success_status_code:
            success_status_code = [200]
        elif not isinstance(success_status_code, list):
            success_status_code = [success_status_code]

        req = requests.get(self.link)

        if req.status_code in success_status_code:
            if destination and isinstance(destination, str):
                File(destination).write(req.text, overwrite=True)

            return req.text

        raise ValueError(
            f"<status_code> ({req.status_code}) not in the <success_status_code> list."
        )
