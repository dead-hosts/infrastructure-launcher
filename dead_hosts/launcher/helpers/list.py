"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides a way to manipulate :code:`list`.

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

import dead_hosts.launcher.helpers as helpers


class List:
    """
    Provides a interface for lists manipulation.

    :param list main: The main list.

    :ivar main: The given :code:`main`.
    """

    def __init__(self, main):
        if not isinstance(main, list):
            raise ValueError(f"<main> should be a {type(list)}")

        self.main = main

    @classmethod
    def __sorting_key(cls, index_data):
        """
        Provides a unified way of sorting.
        """

        if isinstance(index_data, str):
            return index_data.lower()

        return index_data

    def format(self):
        """
        Returns a well formatted list which is sorted and without duplicated.
        """

        return sorted(list(set(self.main)), key=self.__sorting_key)

    def merge(self, to_merge, strict=True):
        """
        Merge the given :code:`to_merge` into the given :code:`main`.

        :param list to_merge: The list to merge.
        :param bool strict: Tell us if we have to respect index value or not.

        :rtype: list
        """

        result = []

        if strict:
            for index, data in enumerate(to_merge):
                try:
                    if isinstance(data, dict) and isinstance(self.main[index], dict):
                        result.append(
                            helpers.dict.Dict(self.main[index]).merge(
                                data, strict=strict
                            )
                        )
                    elif isinstance(data, list) and isinstance(self.main[index], list):
                        result.append(List(self.main[index]).merge(data, strict=strict))
                    else:
                        result.append(data)
                except IndexError:
                    result.append(data)
        else:
            result = self.main

            for data in to_merge:
                if data not in result:
                    result.append(data)

        return result
