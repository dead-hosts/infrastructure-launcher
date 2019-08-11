"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides a way to simply manipulate files.

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

from os import path, remove


class File:
    """
    Provides an interface for file manipulation.

    :param str file: A path to the file to work with.
    :param str encoding: The encoding to use while reading or writting :code:`file`.

    :ivar file: The file we currently work with.
    :ivar encoding: The encoding to use.
    """

    def __init__(self, file, encoding="utf-8"):
        self.file = file
        self.encoding = encoding

    def exists(self):
        """
        Checks if the given :code:`self.file` exists.

        :rtype: bool
        """

        return path.isfile(self.file)

    def read(self):
        """
        Reads the given :code:`self.file`.
        """

        with open(self.file, "r", encoding=self.encoding) as file_stream:
            funilrys = file_stream.read()

        return funilrys

    def read_to_list(self):
        """
        Reads the given :code:`self.file` and convert each lines to a :code:`list`.
        """

        return self.read().splitlines()

    def write(self, data, overwrite=False):
        """
        Writes the given :code:`data` into the given :code:`self.file`.

        :param str data: The data to write.
        :param bool overwrite: Should we overwrite the file ?
        """

        if data and isinstance(data, str):
            if overwrite or not self.exists():
                mode = "w"
            else:
                mode = "a"

            with open(self.file, mode, encoding=self.encoding) as file_stream:
                file_stream.write(data)

    def delete(self):
        """
        Deletes the given :code:`self.file` (if exists).
        """

        if self.exists():
            remove(self.file)
