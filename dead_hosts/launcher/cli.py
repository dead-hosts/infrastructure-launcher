"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides everything related to the CLI.

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

import argparse
import logging

import colorama
from PyFunceble.helpers.environment_variable import EnvironmentVariableHelper

from dead_hosts.launcher.__about__ import __version__
from dead_hosts.launcher.orchestration import Orchestration


def tool() -> None:
    """
    Provide our CLI.
    """

    colorama.init(autoreset=True)

    parser = argparse.ArgumentParser(
        description="The launcher of the Dead-Hosts infrastructure.",
        epilog=f"Crafted with {colorama.Style.BRIGHT}{colorama.Fore.RED}♥"
        f"{colorama.Fore.RESET}{colorama.Style.RESET_ALL} "
        f"by {colorama.Style.BRIGHT}{colorama.Fore.CYAN}Nissar Chababy "
        "(@funilrys)",
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
        default=False,
    )

    parser.add_argument(
        "-e",
        "--end",
        help="Declare a test as completely finished and generate `clean.list`.",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--authorize",
        help="Try to authorize the next job.",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-v",
        "--version",
        help="Show the version of and exit.",
        action="version",
        version="%(prog)s " + __version__,
    )

    arguments = parser.parse_args()

    if arguments.debug or EnvironmentVariableHelper("INFRASTRUCTURE_DEBUG").exists():
        debug_level = logging.DEBUG
    else:
        debug_level = logging.INFO

    logging.basicConfig(
        format="[%(asctime)s::%(levelname)s] %(message)s", level=debug_level
    )

    logging.info("Launcher version: %s", __version__)

    Orchestration(end=arguments.end, save=arguments.save, authorize=arguments.authorize)
