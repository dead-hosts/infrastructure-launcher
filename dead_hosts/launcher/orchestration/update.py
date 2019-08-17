"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the update logic. Basically, the update of all files about
the repository, the infrastructure or project.Is

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

from ..configuration import Links, Markers, Paths
from ..configuration import PyFunceble as PyFuncebleConfig
from ..configuration import TravisCI as TravisCIConfig
from ..helpers import Command, Dict, Download, File, Regex


class Update:
    """
    Provides an interface for the updates.

    :param str working_directory: The directory we are working from.

    :ivar working_directory: Same as :code:`working_directory`.
    """

    def __init__(self, working_directory, info_manager):
        self.working_directory = working_directory
        self.info_manager = info_manager

        self.cross_pyfunceble_config_file = File(
            self.working_directory
            + Links.cross_pyfunceble_configuration["link"].split("/")[-1]
        )
        self.pyfunceble_config_file = File(
            self.working_directory + Links.cross_pyfunceble_configuration["destination"]
        )

        logging.info(
            f"Cross repository PyFunceble config file: {self.cross_pyfunceble_config_file.file}"
        )
        logging.info(f"Local config file: {self.pyfunceble_config_file.file}")

        self.pyfunceble_config()
        self.pyfunceble_official_config()
        self.pyfunceble_official_license()

        self.readme()
        self.our_license()
        self.travis_yml()

    def get_final_commit_message(self):
        """
        Provides the final and update commit message.
        """

        if self.info_manager.ping:
            return (
                PyFuncebleConfig.travis_autosave_final_commit
                + f" | cc {self.info_manager.get_ping_for_commit()} | "
            )
        return PyFuncebleConfig.travis_autosave_final_commit

    def __cross_pyfunceble_config(self):
        """
        Updates the cross configuration of PyFunceble.
        """

        if self.cross_pyfunceble_config_file.exists():
            logging.info("Cross repository file exists locally. Let's update it.")

            upstream_string_version = Download(
                Links.pyfunceble_official_config["link"]
            ).text(destination=None)

            local_version = Dict.from_yaml_string(upstream_string_version)
            local_version = Dict(local_version).merge(
                {
                    x: y
                    for x, y in PyFuncebleConfig.__dict__.items()
                    if not x.startswith("_")
                },
                strict=True,
            )

            local_version_2 = local_version.copy()

            if self.info_manager.ping:
                logging.info("Ping names given, appending them to the commit message.")

                local_version_2[
                    "travis_autosave_final_commit"
                ] = self.get_final_commit_message()

            if self.info_manager.custom_pyfunceble_config and isinstance(
                self.info_manager.custom_pyfunceble_config, dict
            ):
                logging.info(
                    "Custom PyFunceble configuration given, "
                    "appending them to the local configuration file."
                )
                local_version_2 = Dict(local_version_2).merge(
                    self.info_manager.custom_pyfunceble_config, strict=True
                )

            Dict(local_version).to_yaml(
                destination=self.cross_pyfunceble_config_file.file
            )
            Dict(local_version_2).to_yaml(destination=self.pyfunceble_config_file.file)
            logging.info(
                "Finished update of the cross repository PyFunceble config file."
            )
            logging.info("Updated the local PyFunceble configuration too.")

    def pyfunceble_config(self):
        """
        Updates the PyFunceble cross repository configuration.
        """

        self.__cross_pyfunceble_config()

        if (
            not self.info_manager.own_management
            and not self.cross_pyfunceble_config_file.exists()
        ):
            logging.info(
                "Cross repository file dooesn't exists locally. "
                "Let's fetch it into our local PyFunceble config."
            )

            cross_repository_version = Download(
                Links.cross_pyfunceble_configuration["link"]
            ).text(destination=None)

            local_version = Dict().from_yaml_string(cross_repository_version)

            if self.info_manager.ping:
                local_version[
                    "travis_autosave_final_commit"
                ] = self.get_final_commit_message()
                logging.info("Ping names given, appending them to the commit message.")

            if self.info_manager.custom_pyfunceble_config and isinstance(
                self.info_manager.custom_pyfunceble_config, dict
            ):
                logging.info(
                    "Custom PyFunceble configuration given, "
                    "appending them to the local configuration file."
                )
                local_version = Dict(local_version).merge(
                    self.info_manager.custom_pyfunceble_config, strict=True
                )

            logging.debug(f"Interpreded PyFunceble config: {local_version}")

            Dict(local_version).to_yaml(destination=self.pyfunceble_config_file.file)

    def readme(self):
        """
        Updates the README file.
        """

        destination_file_instance = File(self.working_directory + Paths.readme_filename)

        if destination_file_instance.exists():
            logging.info(
                f"{destination_file_instance.file} exists, let's update it's content."
            )

            updated_version = Regex(
                destination_file_instance.read(), Markers.extract_about_pyfunceble
            ).replace(Markers.about_pyfunceble)
            logging.info(
                f"Updated `About PyFunceble` section of {destination_file_instance.file}"
            )

            updated_version = Regex(
                updated_version, Markers.extract_about_dead_hosts
            ).replace(Markers.about_dead_hosts)
            logging.info(
                f"Updated `About Dead-Hosts` section of {destination_file_instance.file}"
            )

            destination_file_instance.write(updated_version, overwrite=True)

    def our_license(self):
        """
        Updates the local version of our LICENSE file.
        """

        Download(Links.our_license["link"]).text(
            destination=self.working_directory + Links.our_license["destination"]
        )
        logging.info(
            f"Updated {self.working_directory + Links.our_license['destination']}"
        )

    def pyfunceble_official_config(self):
        """
        Update the official version of the PyFunceble file.
        """

        Download(Links.pyfunceble_official_config["link"]).text(
            destination=self.working_directory
            + Links.pyfunceble_official_config["destination"]
        )

        logging.info(
            f"Updated {self.working_directory +  Links.pyfunceble_official_config['destination']}"
        )

    def pyfunceble_official_license(self):
        """
        Update the official version of the PyFunceble license.
        """

        Download(Links.pyfunceble_official_license["link"]).text(
            destination=self.working_directory
            + Links.pyfunceble_official_license["destination"]
        )

        logging.info(
            f"Updated {self.working_directory +  Links.pyfunceble_official_license['destination']}"
        )

    def travis_yml(self):
        """
        Updates the `.travis.yml` file.
        """

        if (
            TravisCIConfig.build_dir
            and TravisCIConfig.github_token
            and not File(self.working_directory + "info.example.json").exists()
        ):

            destination = self.working_directory + Paths.travis_filename
            destination_file_instance = File(destination)

            logging.info(f"Updating {destination_file_instance.file}.")
            logging.debug(
                f"{destination_file_instance.file} exists: {destination_file_instance.exists()}"
            )

            content = Dict().from_yaml_string(destination_file_instance.read())
            content = Dict(content).merge(TravisCIConfig.unified_config, strict=True)

            to_write = Dict(content).to_yaml()

            logging.debug(
                f"New repository TravisCI configuration (interpreted): \n{content}"
            )
            destination_file_instance.write(to_write, overwrite=True)

            git_status = Command(
                f"git status '{destination_file_instance.file}' --porcelain",
                print_to_stdout=False,
            ).execute()

            logging.debug(f"GIT states: {git_status}")

            if git_status.strip().startswith("M"):
                logging.info(
                    f"{destination_file_instance.file} changed. Commit and push new version."
                )
                commands = [
                    "git add --all",
                    f"git commit -m '{Markers.maintenance_commit_message}'"
                    f"git push origin {TravisCIConfig.git_branch}",
                ]

                for command in commands:
                    Command(command, print_to_stdout=True).execute()

                exit(0)
