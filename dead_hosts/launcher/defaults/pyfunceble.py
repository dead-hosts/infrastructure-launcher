"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides our default pyfunceble settings.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Project link:
    https://github.com/dead-hosts/infrastructure-launcher

License:
::

    MIT License

    Copyright (c) 2019, 2020, 2021 Dead Hosts
    Copyright (c) 2019, 2020. 2021 Nissar Chababy

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

from PyFunceble.cli.continuous_integration.github_actions import GitHubActions

import dead_hosts.launcher.defaults.envs
import dead_hosts.launcher.defaults.paths

# pylint: disable=line-too-long

CONFIGURATION: dict = {
    "cli_testing.ci.active": GitHubActions().guess_all_settings().authorized,
    "cli_testing.ci.end_command": "hash dead_hosts_launcher && dead_hosts_launcher --end",
    "cli_testing.ci.command": "hash dead_hosts_launcher && dead_hosts_launcher --save",
    "cli_testing.ci.max_exec_minutes": 15,
    "cli_testing.ci.branch": dead_hosts.launcher.defaults.envs.GIT_BRANCH,
    "cli_testing.ci.distribution_branch": dead_hosts.launcher.defaults.envs.GIT_DISTRIBUTION_BRANCH,
    "cli_testing.ci.commit_message": f"[Autosave][Dead-Hosts::"
    f"{dead_hosts.launcher.defaults.paths.GIT_BASE_NAME}]",
    "cli_testing.ci.end_commit_message": f"[Final/Result][Dead-Hosts::"
    f"{dead_hosts.launcher.defaults.paths.GIT_BASE_NAME}]",
    "cli_testing.display_mode.dots": True,
    "cli_testing.display_mode.all": True,
    "cli_testing.display_mode.less": False,
    "cli_testing.file_generation.plain": True,
    "cli_testing.file_generation.hosts": False,
    "cli_testing.file_generation.unified_results": False,
    "cli_testing.cooldown_time": 1.25,
    "cli_testing.display_mode.execution_time": True,
    "cli_testing.max_workers": 1,
    "lookup.timeout": 5,
    "share_logs": False,
    "dns.server": ["8.8.8.8", "8.8.4.4"],
    "dns.protocol": "UDP",
    "cli_testing.preload_file": True,
    "cli_testing.autocontinue": True,
}

PERSISTENT_CONFIG: dict = {
    "cli_testing.autocontinue": True,
    "cli_testing.ci.max_exec_minutes": 20,
    "cli_testing.cooldown_time": 3.25,
    "cli_testing.display_mode.execution_time": True,
    "cli_testing.max_workers": None,
    "cli_testing.preload_file": True,
    "collection.push": True,
    "collection.url_base": "https://collection.dead-hosts.funilrys.com",
    "lookup.collection": True,
}
