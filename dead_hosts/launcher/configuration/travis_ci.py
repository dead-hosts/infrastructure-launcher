"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the TravisCI related configuration.

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

from os import environ

from .paths import Paths


class TravisCI:
    """
    Provides some configuration related to what we do with Travis CI.
    """

    if "TRAVIS_BUILD_DIR" in environ:
        build_dir = environ["TRAVIS_BUILD_DIR"] + Paths.directory_separator
    else:
        build_dir = None
        """
        Provides the build directory.
        """

    if "GH_TOKEN" in environ:
        github_token = environ["GH_TOKEN"]
    else:
        github_token = None
        """
        Provides the github token.
        """

    if "TRAVIS_REPO_SLUG" in environ:
        repo_slug = environ["TRAVIS_REPO_SLUG"]
    else:
        repo_slug = None
        """
        Provides the repository slug.
        """

    if "GIT_EMAIL" in environ:
        git_email = environ["GIT_EMAIL"]
    else:
        git_email = None
        """
        Provides the Git email to use.
        """

    if "GIT_NAME" in environ:
        git_name = environ["GIT_NAME"]
    else:
        git_name = None
        """
        Provides the Git name to use.
        """

    if "GIT_BRANCH" in environ:
        git_branch = environ["GIT_BRANCH"]
    else:
        git_branch = "master"
        """
        Provides the Git branch to use.
        """

    unified_config = {
        "env": {"matrix": ['PYTHON_VERSION="3.7.3"']},
        "language": "generic",
        "sudo": "required",
        "os": ["linux"],
        "addons": {"apt": {"packages": ["dos2unix"]}},
        "install": [
            'export PATH="${HOME}/miniconda/bin:${PATH}"',
            # pylint: disable=line-too-long
            "wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh",
            "bash miniconda.sh -b -p ${HOME}/miniconda",
            "hash -r",
            "conda config --set always_yes yes --set changeps1 no",
            "conda update -q conda",
            'conda create -q -n launcher-environment python="${PYTHON_VERSION}"',
            "source activate launcher-environment",
            "python -VV",
            "pip --version",
            "pip install dead-hosts-launcher",
            "rm miniconda.sh",
        ],
        "script": ["dead_hosts_launcher --version", "dead_hosts_launcher"],
        "notifications": {
            "email": {
                "recipients": ["dead-hosts@funilrys.com"],
                "on_success": "never",
                "on_failure": "always",
            }
        },
    }
    """
    Provides what we want into the configuration file.
    """
