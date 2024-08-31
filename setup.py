"""
Dead Hosts's launcher - The launcher of the Dead-Hosts infrastructure.

Author:
    Nissar Chababy, @funilrys, contactTATAfunilrysTODTODcom

Project link:
    https://github.com/dead-hosts/infrastructure-launcher

License:
::

    MIT License

    Copyright (c) 2019, 2020, 2021, 2022, 2023, 2024 Dead Hosts Contributors
    Copyright (c) 2019, 2020. 2021, 2022, 2023, 2024 Nissar Chababy

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

import re

from setuptools import find_namespace_packages, setup

NAMESPACE = "dead_hosts"
MODULE = "launcher"

PYPI_NAME = f"{NAMESPACE}-{MODULE}".replace("_", "-")


def get_requirements():
    """
    Extracts all requirements from requirements.txt.
    """

    with open("requirements.txt", encoding="utf-8") as file:
        requirements = file.read().splitlines()

    return requirements


def get_version():
    """
    Extracts the version from {NAMESPACE}/{MODULE}/__about__.py
    """

    with open(f"{NAMESPACE}/{MODULE}/__about__.py", encoding="utf-8") as file_stream:
        to_match = re.compile(r'__version__\s=\s"(.*)"')
        extracted = to_match.findall(file_stream.read())[0]

    return ".".join(list(filter(lambda x: x.isdigit(), extracted.split("."))))


def get_long_description():  # pragma: no cover
    """
    Returns the long description.
    """

    with open("README.rst", encoding="utf-8") as file_stream:
        return file_stream.read()


if __name__ == "__main__":
    setup(
        name=PYPI_NAME,
        version=get_version(),
        install_requires=get_requirements(),
        description="The launcher of the Dead-Hosts infrastructure.",
        long_description=get_long_description(),
        license="MIT",
        url="https://github.com/dead-hosts/infrastructure-launcher",
        platforms=["any"],
        packages=find_namespace_packages(),
        include_package_data=True,
        keywords=["Python", "infrastructure", "dead-hosts"],
        classifiers=[
            "Environment :: Console",
            "Topic :: Internet",
            "Development Status :: 5 - Production/Stable",
            "Intended Audience :: Developers",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
        ],
        entry_points={
            "console_scripts": [
                "dead_hosts_launcher=dead_hosts.launcher.cli:tool",
                "dead-hosts-launcher=dead_hosts.launcher.cli:tool",
                "dh_launcher=dead_hosts.launcher.cli:tool",
                "dh-launcher=dead_hosts.launcher.cli:tool",
            ]
        },
    )
