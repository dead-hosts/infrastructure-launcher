"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides our default paths.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Project link:
    https://github.com/dead-hosts/infrastructure-launcher

License:
::

    MIT License

    Copyright (c) 2019, 2020, 2021, 2022, 2023, 2024 Dead Hosts Contributors
    Copyright (c) 2019, 2020. 2021, 2022, 2023, 2024 Nissar Chababy

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
import urllib.parse
from datetime import datetime
from typing import List

from dead_hosts.launcher.command import Command

CURRENT_DIRECTORY: str = os.getcwd()

GHA_WORKFLOW_DIR: str = os.path.join(".github", "workflows")
PYFUNCEBLE_NAMESPACE: str = ".pyfunceble"
PYFUNCEBLE_CONFIG_DIRECTORY: str = os.path.join(CURRENT_DIRECTORY, PYFUNCEBLE_NAMESPACE)

GHA_WORKFLOW_LOCAL_HASHES_FILENAME: str = "hs.json"
INFO_FILENAME: str = "info.json"
ORIGIN_FILENAME: str = "origin.list"
INPUT_FILENAME: str = "domains.list"
OUTPUT_FILENAME: str = "clean.list"
README_FILENAME: str = "README.md"

EXAMPLE_INFO_FILENAME: str = "info.example.json"

REMOTE_URL: str = Command("git remote get-url origin").execute().strip()
PARSED_REMOTE_URL: str = urllib.parse.urlparse(REMOTE_URL)

if not PARSED_REMOTE_URL.netloc:
    REPO_BASE = PARSED_REMOTE_URL.path.split(":", 1)[-1]
else:
    REPO_BASE = PARSED_REMOTE_URL.path[1:]

if REPO_BASE.endswith(".git"):
    REPO_BASE = REPO_BASE[:-4]

GIT_BASE_NAME: str = REPO_BASE.split("/", 1)[-1]
GIT_REPO_OWNER: str = REPO_BASE.split("/", 1)[0]

OUTPUT_FILE_HEADER: List[str] = [
    "# File generated by the Dead-Hosts project with the help of PyFunceble.",
    "# Dead-Hosts: https://github.com/dead-hosts",
    "# PyFunceble: https://pyfunceble.github.io",
    f"# Generation Time: {datetime.utcnow().isoformat()}",
]
