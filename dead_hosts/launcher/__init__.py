"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the launcher logic.

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

from argparse import ArgumentParser
from os import environ

from colorama import Fore, Style
from colorama import init as init_colorama

from .orchestration import Orchestration

VERSION = "0.0.5"


def command_line():
    """
    Provides the CLI.
    """

    init_colorama(autoreset=True)

    parser = ArgumentParser(
        description="The launcher of the Dead-Hosts infrastructure.",
        epilog=f"Crafted with {Style.BRIGHT + Fore.RED}♥{Fore.RESET + Style.RESET_ALL} "
        f"by {Style.BRIGHT + Fore.CYAN}Nissar Chababy (@funilrys)",
    )

    parser.add_argument(
        "-d",
        "--debug",
        help="Activate the logging in verbose mode..",
        action="store_true",
    )

    parser.add_argument(
        "-s",
        "--save",
        help="Declare a test as " "'to be continued'.",
        action="store_true",
    )

    parser.add_argument(
        "-e",
        "--end",
        help="Declare a test as completly finished and generate `clean.list`.",
        action="store_true",
    )

    parser.add_argument(
        "-v",
        "--version",
        help="Show the version of and exit.",
        action="version",
        version="%(prog)s " + VERSION,
    )

    arguments = parser.parse_args()

    debug = arguments.debug or (
        "INFRASTRUCTURE_DEBUG" in environ and environ["INFRASTRUCTURE_DEBUG"]
    )

    Orchestration(end=arguments.end, save=arguments.save, debug=debug)
