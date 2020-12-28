"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the updater of the Travis CI configuration.

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

import logging
import os

from PyFunceble.helpers.dict import DictHelper
from PyFunceble.helpers.file import FileHelper
from PyFunceble.helpers.merge import Merge

import dead_hosts.launcher.defaults.markers
import dead_hosts.launcher.defaults.paths
import dead_hosts.launcher.defaults.travis_ci
from dead_hosts.launcher.updater.base import UpdaterBase


class TravisCIConfigUpdater(UpdaterBase):
    """
    Provides the updater of the Travis CI configuration file.
    """

    DESTINATION: FileHelper = FileHelper(
        os.path.join(
            dead_hosts.launcher.defaults.travis_ci.BUILD_DIR,
            dead_hosts.launcher.defaults.paths.TRAVIS_CONFIG_FILENAME,
        )
    )

    @property
    def authorized(self) -> bool:
        return (
            dead_hosts.launcher.defaults.travis_ci.UPDATE_CI_CONFIG
            and dead_hosts.launcher.defaults.travis_ci.GITHUB_TOKEN
            and not FileHelper(
                os.path.join(
                    dead_hosts.launcher.defaults.travis_ci.BUILD_DIR,
                    "info.example.json",
                )
            )
        )

    def pre(self) -> "TravisCIConfigUpdater":
        logging.info("Started to update %r!", self.DESTINATION.path)

        return self

    def post(self) -> "TravisCIConfigUpdater":
        logging.info("Finished to update %r!", self.DESTINATION.path)

        return self

    @staticmethod
    def clean_main(content: dict) -> dict:
        """
        Given the content of the Travis CI configuration file,
        we clean the main entries.
        """

        to_delete = ["cache", "matrix", "python", "sudo", "addons"]

        for index in to_delete:
            if index in content:
                del content[index]

        return content

    @staticmethod
    def clean_global_env(content: dict) -> dict:
        """
        Given the content of the Travis CI configuration file, we clean the
        :code:`env.global` entries`.
        """

        to_delete = [
            "UPDATE_ME_LOCATION",
            "ADMIN_LOCATION",
            "TRAVIS_REPO_SLUG",
        ]

        if "env" in content and "global" in content["env"]:
            for index, data in enumerate(content["env"]["global"]):
                for env_var in to_delete:
                    if env_var in data:
                        del content["env"]["global"][index]

        return content

    @staticmethod
    def clean_env(content: dict) -> dict:
        """
        Given the content of the Travis CI configuration file,
        we clean the env entries.
        """

        to_delete = ["matrix"]

        if "env" in content:
            for env_var in to_delete:
                if env_var in content["env"]:
                    del content["env"][env_var]

        return content

    @staticmethod
    def update_global(content: dict) -> dict:
        """
        Given the content of the Travis configuration file,
        we update the env.global entries.
        """

        to_update = {
            "GIT_NAME": "Dead-Hosts",
            "GIT_EMAIL": dead_hosts.launcher.defaults.travis_ci.DEFAULT_EMAIL,
        }
        to_add = {"PYTHON_VERSION": "3.8.0"}

        if "env" in content and "global" in content["env"]:
            for index, data in enumerate(content["env"]["global"]):
                for env_var, value in to_update.items():
                    if env_var in data and data[env_var] != value:
                        content["env"]["global"][index][env_var] = value

            for env_var, value in to_add.items():
                if any([env_var in x for x in content["env"]["global"]]):
                    continue

                content["env"]["global"].append({env_var: value})

        return content

    def start(self) -> "TravisCIConfigUpdater":
        content = DictHelper().from_yaml_file(self.DESTINATION.path)
        content = Merge(dead_hosts.launcher.defaults.travis_ci.UNIFIED_CONFIG).into(
            content
        )

        content = self.update_global(
            self.clean_env(self.clean_global_env(self.clean_main(content)))
        )

        DictHelper(content).to_json_file(self.DESTINATION.path)

        logging.debug("New Travis CI configuration (interpreter):\n%s", content)

        return self
