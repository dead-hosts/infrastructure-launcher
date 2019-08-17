"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the paths we have to work with.

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

from os import getcwd, sep


class Paths:
    """
    Provides some paths related configuration.
    """

    directory_separator = sep
    """
    Set the current directory separator.
    """

    current_directory = getcwd() + directory_separator
    """
    Provides the current directory.
    """

    info_filename = "info.json"
    """
    Provides the filename of our admin file.
    """

    origin_filename = "origin.list"
    """
    Provides the filename we will use to save the original file (from upstream)
    """

    input_filename = "domains.list"
    """
    Provides the filename we have to read.
    """

    output_filename = "clean.list"
    """
    Provides the filename we generate after a test of a list is done.
    """

    readme_filename = "README.md"
    """
    Provides the filename of our README.
    """

    travis_filename = ".travis.yml"
    """
    Provides the filename of our .travis.yml file.
    """
