"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides a way to manipulate :code:`dict`.

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

from io import TextIOWrapper
from json import decoder, dump, dumps, load, loads

from yaml import dump as yaml_dump
from yaml import safe_load as yaml_load

import dead_hosts.launcher.helpers as helpers


class Dict:
    """
    Provides a interface for dictionaries manipulation.

    :param dict main: The main dictionary.

    :ivar main: The givne :code:`main`.
    """

    def __init__(self, main=None):
        self.main = main

    def to_json(self, destination=None, encoding="utf-8"):
        """
        Converts :code:`self.main` into a JSON formatted string.

        :param str destination: A destination to save the JSON string.
        :param str encoding: The encoding to use if we save the JSON string into a file.

        :rtype: str, None
        """

        if destination:
            with open(destination, "w", encoding=encoding) as file_stream:
                return dump(
                    self.main, file_stream, ensure_ascii=False, indent=4, sort_keys=True
                )
        return dumps(self.main, ensure_ascii=False, indent=4, sort_keys=True)

    def to_yaml(self, destination=None, encoding="utf-8", flow_style=False):
        """
        Converts :code:`self.main` into a YAML formatted string.

        :param str destination: A destination to save the YAML formatted string.
        :param str encoding: The encoding to use.
        :param bool flow_style: Tell us to follow or not the default flow style.

        :rtype: str, NOne
        """

        if destination:
            with open(destination, "w", encoding=encoding) as file_stream:
                return yaml_dump(
                    self.main,
                    file_stream,
                    encoding=encoding,
                    allow_unicode=True,
                    indent=4,
                    default_flow_style=flow_style,
                )
        return yaml_dump(
            self.main,
            encoding=encoding,
            allow_unicode=True,
            indent=4,
            default_flow_style=flow_style,
        )

    @classmethod
    def from_json_string(cls, data):
        """
        Converts the given JSON string (:code:`data`) into a :code:`dict`.

        :param str data: The JSON string to convert to :code:`dict`.

        :rtype: dict
        """

        try:
            return loads(data)
        except decoder.JSONDecodeError:
            return {}

    @classmethod
    def from_json_file(cls, file, encoding="utf-8"):
        """
        Converts the given JSON file (:code:`file`) into a :code:`dict`.

        :param file: The JSON file to convert to :code:`dict`.
        :type file: TextIOWrapper, str

        :param str encoding: The encoding to use while opening the file path.

        :rtype: dict
        """

        if isinstance(file, TextIOWrapper):
            return load(file)

        with open(file, "r", encoding=encoding) as file_stream:
            return load(file_stream)

    @classmethod
    def from_yaml_string(cls, data):
        """
        Converts the given YAML string (:code:`data`) into a :code:`dict`.

        :param str data: The YAML string to convert to :code:`dict`.

        :rtype: dict
        """

        return yaml_load(data)

    @classmethod
    def from_yaml_file(cls, file, encoding="utf-8"):
        """
        Converts the given YAML file (:code:`file`) into a :code:`dict`.

        :param file: The YAML file to convert to :code:`dict`.
        :type file: TextIOWrapper, str

        :param str encoding: The encoding to use while opening the file path.

        :rtype: dict
        """

        if isinstance(file, TextIOWrapper):
            return yaml_load(file)

        with open(file, "r", encoding=encoding) as file_stream:
            return yaml_load(file_stream)

    def merge(self, to_merge, strict=True):
        """
        Merge the given :code:`to_merge` into the given :code:`main`.

        :param dict to_merge: The :code:`dict` to merge.
        :param bool strict: Tell us if we have to respect index value or not while mergin lists.

        :rtype: dict
        """

        result = {}

        for index, data in to_merge.items():
            if index in self.main:
                if isinstance(data, dict) and isinstance(self.main[index], dict):
                    result[index] = Dict(self.main[index]).merge(data, strict=strict)
                elif isinstance(data, list) and isinstance(self.main[index], list):
                    result[index] = helpers.list.List(self.main[index]).merge(
                        data, strict=strict
                    )
                else:
                    result[index] = data
            else:
                result[index] = data

        for index, data in self.main.items():
            if index not in result:
                result[index] = data

        return result
