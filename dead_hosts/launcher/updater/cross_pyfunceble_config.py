"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the updater of the cross-repository PyFunceble configuration.

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

from ..configuration import Links
from ..configuration import PyFunceble as PyFuncebleConfig
from ..configuration import TravisCI as TravisCIConfig
from .base import Base


class CrossPyFuncebleConfigUpdater(Base):
    """
    Provides the updater of the cross-repository PyFunceble configuration.
    """

    def __init__(self) -> None:
        self.do_not_start = True
        super().__init__()

        self.cross_pyfunceble_config_file = pyfunceble_helpers.File(
            self.working_dir
            + Links.cross_pyfunceble_configuration["link"].split("/")[-1]
        )

        self.pyfunceble_config_file = pyfunceble_helpers.File(
            self.working_dir + Links.cross_pyfunceble_configuration["destination"]
        )

        self.start_after_authorization()

    @classmethod
    def get_commit_message(cls, pings: Optional[str] = None) -> str:
        """
        Provides the commit message.
        """

        if pings:
            return f"{PyFuncebleConfig.ci_autosave_final_commit} | cc {pings} | "
        return PyFuncebleConfig.ci_autosave_final_commit

    def authorization(self) -> bool:
        return (
            self.cross_pyfunceble_config_file.exists() or not TravisCIConfig.git_email
        )

    def pre(self):
        logging.info(
            "Started to update %s and %s",
            self.cross_pyfunceble_config_file.path,
            self.pyfunceble_config_file.path,
        )

    def post(self):
        logging.info(
            "Finished to update %s and %s",
            self.cross_pyfunceble_config_file.path,
            self.pyfunceble_config_file.path,
        )

    def start(self):
        upstream_data = pyfunceble_helpers.Download(
            Links.pyfunceble_official_config["link"]
        ).text()

        local_version = pyfunceble_helpers.Dict.from_yaml(upstream_data)
        local_version = pyfunceble_helpers.Merge(
            {
                x: y
                for x, y in PyFuncebleConfig.__dict__.items()
                if not x.startswith("_")
            }
        ).into(local_version, strict=True)

        local_version_copy = local_version.copy()

        if self.info_manager.ping:
            logging.info("Ping names given, appending them to the commit message.")

            local_version_copy["ci_autosave_final_commit"] = self.get_commit_message(
                pings=self.info_manager.get_ping_for_commit()
            )

        if self.info_manager.custom_pyfunceble_config and isinstance(
            self.info_manager.custom_pyfunceble_config, dict
        ):
            logging.info(
                "Custom PyFunceble configuration given, "
                "appending them to the local configuration file."
            )

            local_version_copy = pyfunceble_helpers.Merge(
                self.info_manager.custom_pyfunceble_config
            ).into(local_version_copy, strict=True)

        pyfunceble_helpers.Dict(local_version).to_yaml_file(
            self.cross_pyfunceble_config_file.path
        )
        pyfunceble_helpers.Dict(local_version_copy).to_yaml_file(
            self.pyfunceble_config_file.path
        )
