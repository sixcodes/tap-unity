#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="tap-unity",
    version="0.2.0"
            "",
    description="Singer.io tap for extracting data from Unity API",
    author="Jesue Junior <jesuesousa@gmail.com>",
    url="http://singer.io",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_unity"],
    install_requires=[
        # NB: Pin these to a more specific version for tap reliability
        "singer-python",
        "requests",
    ],
    entry_points="""
    [console_scripts]
    tap-unity=tap_unity:main
    """,
    packages=find_packages(),
    package_data = {
        "tap_unity": ["schemas/*.json"]
    }
)
