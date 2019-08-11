"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides a simple implementation of the python :code:`re` package.

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

from re import compile as comp
from re import escape as esc
from re import sub


class Regex:
    """
    Provides a simple implementation of the python :code:`re` package.

    :param data: The data to work with.
    :type data: str, list
    :param str regex: The regex to work with.
    :param bool escape: Should we escape the given :code:`regex`?

    :ivar regex: The regex we work with.
    :ivar data: The data we work with.
    """

    def __init__(self, data, regex, escape=False):
        self.data = data

        if escape:
            self.regex = esc(regex)
        else:
            self.regex = regex

    def get_not_matching_list(self):
        """
        Returns a list of string which don't match the given :code:`regex`.

        .. warning::
            We expect :code:`self.data` to be a list of string.
        """

        pre_result = comp(self.regex)

        return [x for x in self.data if not pre_result.search(x)]

    def get_matching_list(self):
        """
        Returns a list of string which match the given :code:`regex`.

        .. warning::
            We expect :code:`self.data` to be a list of string.
        """

        pre_result = comp(self.regex)

        return [x for x in self.data if pre_result.search(x)]

    def match(self, rematch=False, return_data=True, group=0):
        """
        Checks if the given :code:`data` matches the given :code:`regex`.

        :param bool rematch:
            Return the matched group into a formatted list.

            .. note::
                This allows us to have an implementation of the Bash :code:`${BASH_REMATCH}`.
        :param bool return_data:
            Tell us to return what was matched.
        :param int group:
            The index of the group to return.

        :rtype: str, list, bool
        """

        to_match = comp(self.regex)

        if rematch:
            pre_result = to_match.findall(self.data)
        else:
            pre_result = to_match.search(self.data)

        if return_data and pre_result:
            if rematch:
                result = []

                for data in pre_result:
                    if isinstance(data, tuple):
                        result.extend(list(data))
                    else:
                        result.append(data)

                if group != 0:
                    return result[group]
                return result
            return pre_result.group(group).strip()

        if not return_data and pre_result:
            return True
        return False

    def replace(self, replacement, occurences=0):
        """
        Replaces the matched part with the given :code:`replacement`.

        :param str replacement: The replacement.
        :param int occurences:
            The number of occurences to replace.

            .. note::
                If :code:`0` is given, we replace every occurences.

        :rtype: str
        """

        if replacement:
            return sub(self.regex, replacement, self.data, occurences)
        return self.data
