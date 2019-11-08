"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides a way to run Shell commands.

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


from os import environ
from subprocess import PIPE, STDOUT, Popen


class Command:
    """
    Provides an interface to run shell commands.

    :param str command: The command to execute.
    :param bool print_to_stdout: Allow/disallow the output to stdout.
    :param str encoding: The encoding to use to decode the shell output.

    :ivar command: The given :code:`command`.
    :ivar allow_stdout: The given :code:`print_to_stdout`.
    :ivar encoding: The given :code:`encoding`.
    :ivar process: The :code:`Popen` instance we use to execute the command.
    """

    def __init__(self, command, print_to_stdout=False, encoding="utf-8"):
        self.command = command
        self.allow_stdout = print_to_stdout
        self.encoding = encoding

        if not self.allow_stdout:
            self.process = Popen(
                self.command, stdout=PIPE, stderr=STDOUT, shell=True, env=environ
            )
        else:
            self.process = Popen(self.command, stderr=STDOUT, shell=True, env=environ)

    def __decode_output(self, to_decode):
        """
        Decodes the given command output.

        :param bytes to_decode: The command output to decode.

        :rtype: str, None, Bool
        :return:
            A :code:`str`, when a :code:`bytes` is given and the given :code:`to_decode`
            for everything else.
        """

        if isinstance(to_decode, bytes):
            return to_decode.decode(self.encoding)

        return to_decode

    def execute(self):
        """
        Executes the given command.
        """

        (stdout, stderr) = self.process.communicate()

        if self.process.returncode != 0:
            decoded = self.__decode_output(stderr)

            raise Exception(decoded)
        return self.__decode_output(stdout)
