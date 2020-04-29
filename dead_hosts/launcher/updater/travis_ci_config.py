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
from typing import Optional

import PyFunceble.helpers as pyfunceble_helpers
from PyFunceble.exceptions import GitHubTokenNotFound

from ..configuration import Paths
from ..configuration import TravisCI as TravisCIConfig
from .base import Base


class TravisCIConfigUpdater(Base):
    """
    Provides the updater of the Travis CI configuration.
    """

    destination: Optional[pyfunceble_helpers.File] = None

    def __init__(self) -> None:

        self.do_not_start = True

        super().__init__()

        if (
            not pyfunceble_helpers.File(f"{self.working_dir}info.example.json").exists()
            and TravisCIConfig.build_dir
            and not TravisCIConfig.github_token
        ):
            raise GitHubTokenNotFound()

        self.start_after_authorization()

    def authorization(self):
        return (
            TravisCIConfig.update_ci_config
            and TravisCIConfig.build_dir
            and TravisCIConfig.github_token
            and not pyfunceble_helpers.File(
                f"{self.working_dir}info.example.json"
            ).exists()
        )

    def pre(self):
        self.destination = pyfunceble_helpers.File(
            f"{self.working_dir}{Paths.travis_filename}"
        )
        logging.info("Started to update %s!", self.destination.path)

    def post(self):
        logging.info("Finished to update %s!", self.destination.path)

    @classmethod
    def clean_main(cls, content: dict) -> dict:
        """
        Given the content of the Travis CI configuration file,
        we clean the main entries.
        """

        to_delete = ["cache", "matrix", "python", "sudo", "addons"]

        for index in to_delete:
            if index in content:
                del content[index]

        return content

    @classmethod
    def clean_global_env(cls, content: dict) -> dict:
        """
        Given the content of the Travis CI configuration file,
        we clean the env.global entries.
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

    @classmethod
    def clean_env(cls, content: dict) -> dict:
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

    @classmethod
    def update_global(cls, content: dict) -> dict:
        """
        Given the content of the Travis configuration file,
        we update the env.global entries.
        """

        to_update = {
            "GIT_NAME": "Dead-Hosts",
            "GIT_EMAIL": TravisCIConfig.default_email,
        }
        to_add = {"PYTHON_VERSION": "3.7.5"}

        if "env" in content and "global" in content["env"]:
            for index, data in enumerate(content["env"]["global"]):
                for env_var, value in to_update.items():
                    if env_var in data and data[env_var] != value:
                        content["env"]["global"][index][env_var] = value

            for env_var, value in to_add.items():
                present = [env_var in x for x in content["env"]["global"]]

                if any(present):
                    continue

                content["env"]["global"].append({env_var: value})

        return content

    def start(self) -> None:
        content = pyfunceble_helpers.Dict.from_yaml_file(self.destination.path)
        content = pyfunceble_helpers.Merge(TravisCIConfig.unified_config).into(content)

        content = self.update_global(
            self.clean_env(
                self.clean_env(self.clean_global_env(self.clean_main(content)))
            )
        )

        to_write = pyfunceble_helpers.Dict(content).to_yaml()

        logging.debug("New Travis CI configuration (interpreter):\n%s", content)

        self.destination.write(to_write, overwrite=True)
