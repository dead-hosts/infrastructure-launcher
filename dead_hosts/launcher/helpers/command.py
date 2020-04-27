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

    Copyright (c) 2019, 2020 Dead Hosts
    Copyright (c) 2019, 2020 Nissar Chababy

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

import sys
from os import environ
from subprocess import PIPE, STDOUT, Popen

import PyFunceble.helpers as pyfunceble_helpers


class Command(pyfunceble_helpers.Command):
    """
    Overwrite some methods for our use cases.
    """

    def get_command_output(self):
        """
        Run the given command and return it's output.
        """

        with Popen(
            self.command, stdout=PIPE, stderr=PIPE, shell=True, env=environ
        ) as process:
            output, error = process.communicate()

            if process.returncode != 0:
                decoded = self._decode_output(error)

                if not decoded:
                    return f"Unknown error for {self.command}"
                print(decoded)
                sys.exit(1)
            return self._decode_output(output)

    def run(self, rstrip=True):
        """
        Run the given command and yield each line(s) one by one.

        .. note::
            The difference between this method and :func:`~PyFunceble.helpers.Command.execute`
            is that :func:`~PyFunceble.helpers.Command.execute` wait for the process to end
            in order to return its output while this method return each line one by one
            - as they are outputed.

        :param bool rstrip:
            Deactivates the rstrip of the output.

        :raise Exception: When the exit code is not 0.
        """

        with Popen(
            self.command, stdout=PIPE, stderr=STDOUT, shell=True, env=environ
        ) as process:
            # We initiate a process and parse the command to it.

            while True:
                # We loop infinitly because we want to get the output
                # until there is none.

                # We get the current line from the process stdout.
                #
                # Note: we use rstrip() because we are paranoid :-)
                current_line = process.stdout.readline()

                if not current_line and process.poll() is not None:
                    # The current line is empty or equal to None.

                    # We break the loop.
                    break

                # The line is not empty nor equal to None.

                if rstrip:
                    current_line = current_line.rstrip()

                # We encode and yield the current line
                yield self._decode_output(current_line)

            if process.returncode and process.returncode != 0:
                raise Exception("Something went wrong. Please report to stdout.")
