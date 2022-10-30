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

    Copyright (c) 2019, 2020, 2021, 2022 Dead Hosts
    Copyright (c) 2019, 2020. 2021, 2022 Nissar Chababy

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

import os
import subprocess
from typing import Generator

from PyFunceble.helpers.command import CommandHelper


class Command(CommandHelper):
    """
    Improves PyFunceble's helper for our needs.
    """

    def run(self, rstrip: bool = True) -> Generator[str, None, None]:
        """
        Overwrites the run method. In our implementation we check the status
        code and raise an exception if it not equal to zero.
        """
        with subprocess.Popen(
            self.command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=True,
            env=os.environ,
        ) as process:
            while True:
                # Note: we use rstrip() because we are paranoid :-)
                current_line = process.stdout.readline()

                if not current_line and process.poll() is not None:
                    break

                if rstrip:
                    yield self._decode_output(current_line.rstrip())
                else:
                    yield self._decode_output(current_line)

            if process.returncode != 0:
                raise RuntimeError(
                    "Something went wrong.\n" + self._decode_output(current_line)
                )
