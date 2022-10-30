"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Provides the base of all our updaters.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Project link:
    https://github.com/dead-hosts/infrastructure-launcher

License:
::

    MIT License

    Copyright (c) 2019, 2020, 2021, 2022 Dead Hosts
    Copyright (c) 2019, 2020. 2021, 2022 Nissar Chababy

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

from typing import Optional

from dead_hosts.launcher.info_manager import InfoManager


class UpdaterBase:
    """
    Provides the base of all updates.

    :param info_manager:
        The info manager to work with.

    :raise TypeError:
        When the given :code:`info_manager` is not a real info manager.
    """

    do_not_start: bool = False
    info_manager: Optional[InfoManager] = None

    def __init__(self, info_manager: InfoManager) -> None:
        if not isinstance(info_manager, InfoManager):
            raise TypeError(info_manager)

        self.info_manager = info_manager

        if not self.do_not_start:
            self.start_after_authorization()

    @property
    def authorized(self) -> bool:
        """
        Provides the authorization to process.
        """

        return False

    def pre(self) -> "UpdaterBase":
        """
        Called before :code:`start`.
        """

        raise NotImplementedError()

    def post(self) -> "UpdaterBase":
        """
        Called after :code:`start`.
        """

        raise NotImplementedError()

    def start(self) -> "UpdaterBase":
        """
        Starts the update.
        """

        raise NotImplementedError()

    def start_after_authorization(self) -> "UpdaterBase":
        """
        Starts after checking the authorization.
        """

        if self.authorized:
            self.pre()
            self.start()
            self.post()

        return self
