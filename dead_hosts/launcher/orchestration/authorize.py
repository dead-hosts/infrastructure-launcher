"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the authorization logic.

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

from datetime import datetime, timedelta

import PyFunceble.helpers as helpers

from ..configuration import Markers


class Authorize:
    """
    Provides some authorization logic.

    :param info_manager: An instance of the info manager.

    :ivar info_manager: The info manager.
    """

    def __init__(self, info_manager):
        self.info_manager = info_manager

    @classmethod
    def is_launch_given_by_commit_message(cls):
        """
        Checks if the launch per commit message is valid.
        """

        return helpers.Regex(Markers.launch_test).match(
            helpers.Command("git log -1").execute(), return_match=False
        )

    def refresh(self):
        """
        Provides the refresh authorization.

        If this authorization is not given, we should not update
        modify any files related to the original list we are testing.

        :rtype: bool
        """

        if (
            not self.info_manager.currently_under_test
            or self.is_launch_given_by_commit_message()
        ):
            return True

        return False

    def get_test_authorization_time(self):
        """
        Provides the expected (minimal) date of authorization
        of the next build.
        """

        return self.info_manager.finish_datetime + timedelta(
            days=self.info_manager.days_until_next_test
        )

    def test(self):
        """
        Provides the test authorization.

        If this authorization is not given, we should not start
        the test.

        :rtype: bool
        """

        if self.is_launch_given_by_commit_message():
            return True

        if (
            not self.info_manager.days_until_next_test
            or self.info_manager.days_until_next_test < 0
        ):
            return True

        if datetime.now() > self.get_test_authorization_time():
            return True

        if self.info_manager.currently_under_test:
            return True

        return False
