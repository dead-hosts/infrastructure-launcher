"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the configuration to transfer to PyFunceble.

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

from .paths import Paths
from .travis_ci import TravisCI


class PyFunceble:
    """
    Provides some PyFunceble related configuration.
    """

    # pylint: disable=line-too-long

    idna_conversion = True
    """
    Let PyFunceble know that we want every subjects to be converted in IDNA
    format.
    """

    command_before_end = "hash dead_hosts_launcher && dead_hosts_launcher --end"
    """
    Let PyFunceble know the command it has to run before pushing the final commit.
    """

    command = "hash dead_hosts_launcher && dead_hosts_launcher --save"
    """
    Let PyFunceble know the commant it has to run before pushing (except the final one).
    """

    print_dots = True
    """
    Let PyFunceble know that we want dots to be part of stdout :-)
    """

    generate_complements = False
    """
    Let PyFunceble know that we want to generate/test complements.
    """

    less = False
    """
    Let PyFunceble know that we want less information on screen (or not).
    """

    plain_list_domain = True
    """
    Let PyFunceble know that we want a plain list version.
    """

    timeout = 6
    """
    Let PyFunceble know the timeout to apply to each subject test.
    """

    share_logs = False
    """
    Let PyFunceble know that we want to share the logs.
    """

    split = True
    """
    Let PyFunceble know that we want a splitted logs.
    """

    ci_autosave_minutes = 10
    """
    Let PyFunceble know that we want x minutes between each test.
    """

    ci = TravisCI.build_dir is not None and TravisCI.github_token is not None
    """
    Let PyFunceble know if we are under Travis CI (or not).
    """

    multiprocess = True
    """
    Let PyFunceble know that we want to use the multiprocessing.
    """

    maximal_processes = 2
    """
    Let PyFunceble know how many processs we want to use (if multiprocess) is activated.
    """

    dns_server = ["8.8.8.8", "8.4.4.8"]
    """
    Let PyFunceble know the DNS server we want to user for DNS query.
    """

    ci_branch = TravisCI.git_branch
    """
    Let PyFunceble know the branch to push into.
    """

    ci_distribution_branch = TravisCI.git_distribution_branch
    """
    Let PyFunceble know the branch to push into (for distribution)
    """

    ci_autosave_commit = f"[Autosave][Dead-Hosts::{Paths.git_base_name}]"
    """
    Let PyFunceble know the default autosave commit message.
    """

    ci_autosave_final_commit = f"[Final/Result][Dead-Hosts::{Paths.git_base_name}]"
    """
    Let PyFunceble know the default final commit message.
    """

    @classmethod
    def get_dict(cls):
        """
        Provides the dict version of the variables.
        """

        to_ignore = ["get_dict"]

        return {
            x: y
            for x, y in cls.__dict__.items()
            if not x.startswith("_") and x not in to_ignore
        }
