"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the authorization interface.

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

from datetime import datetime, timedelta

from PyFunceble.helpers.regex import RegexHelper

import dead_hosts.launcher.defaults.markers
from dead_hosts.launcher.command import Command
from dead_hosts.launcher.info_manager import InfoManager


class Authorization:
    """
    Provides the authorization logic.
    """

    def __init__(self, info_manager: InfoManager) -> None:
        self.info_manager = info_manager

    @property
    def next_authorization_time(self):
        """
        Provides the time of the next authorization.
        """

        return self.info_manager.finish_datetime + timedelta(
            days=self.info_manager.days_until_next_test
        )

    @staticmethod
    def is_launch_flag_given_by_commit_message() -> bool:
        """
        Checks if the launch flag per commit message is given.
        """

        return RegexHelper(dead_hosts.launcher.defaults.markers.LAUNCH_TEST).match(
            Command("git log -1").execute(), return_match=False
        )

    def are_we_suppoed_to_always_update_input(self) -> bool:
        """
        Checks if we are supposed to systematically update the input source.
        """

        return self.info_manager.live_update is True

    def is_refresh_authorized(self) -> bool:
        """
        Provides the refresh authorization.

        If this authorization is not given, we should not update
        modify any files related to the original list we are testing.
        """

        return (
            not bool(self.info_manager.currently_under_test)
            or self.is_launch_flag_given_by_commit_message()
            or self.are_we_suppoed_to_always_update_input()
        )

    def is_test_authorized(self) -> bool:
        """
        Provides the test authorization.

        If this authorization is not given, we should not start
        the test.
        """

        if self.is_launch_flag_given_by_commit_message():
            return True

        if (
            not self.info_manager.days_until_next_test
            or self.info_manager.days_until_next_test < 0
        ):
            return True

        if datetime.utcnow() > self.next_authorization_time:
            return True

        if self.info_manager.currently_under_test:
            return True

        return False
