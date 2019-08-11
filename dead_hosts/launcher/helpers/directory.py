"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides a way to simply manipulate directories.

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

from os import mkdir, path
from shutil import rmtree


class Directory:
    """
    Provides an interface for directory manipulation.

    :param str directory: A path to the directory to work with.

    :ivar directory: The directory we currently work with.
    """

    def __init__(self, directory):
        self.directory = directory

    def exists(self):
        """
        Checks if the given :code:`self.file` exists.

        :rtype: bool
        """

        return path.isdir(self.directory)

    def create(self):
        """
        Creates the given directory (if it does not exists).
        """

        if not self.exists():
            mkdir(self.directory)

    def delete(self):
        """
        Deletes the given directory.
        """

        if self.exists():
            rmtree(self.directory)
