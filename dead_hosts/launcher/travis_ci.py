"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides some methods oriented to our business logic with Travis CI.

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

import logging

from .configuration import Paths
from .configuration import TravisCI as Config
from .helpers import Command


class TravisCI:
    """
    Provides some TravisCI related methods.
    """

    @classmethod
    def init_repo(cls):
        """
        Initiates the repository for future push.
        """

        if Config.build_dir and Config.github_token:
            commands = [
                "git remote rm origin",
                f"git remote add origin "
                f"https://{Config.github_token}@github.com/{Config.repo_slug}.git",
                f'git config --global user.email "{Config.git_email}"',
                f'git config --global user.name "{Config.git_name}"',
                "git config --global push.default simple",
                f"git checkout {Config.git_branch}",
            ]

            for command in commands:
                Command(command, print_to_stdout=False).execute()

            logging.info("Git repository prepared for push.")

    @classmethod
    def update_permissions(cls):
        """
        Updates the permissions. Indeed as we had some bad time in the past we do this
        almost systematically.
        """

        if Config.build_dir and Config.github_token:
            commands = [
                f"sudo chown -R travis:travis {Config.build_dir}",
                f"sudo chmod -R g+rwX {Config.build_dir}",
                f"sudo chmod 777 -Rf {Config.build_dir + Paths.directory_separator}.git",
                f"sudo find {Config.build_dir} -type d -exec chmod g+x " "'{}' \\;'",
            ]

            for command in commands:
                Command(command, print_to_stdout=False).execute()

            logging.info("Updated files and directories permissions.")
