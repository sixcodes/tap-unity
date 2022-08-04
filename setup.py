#!/usr/bin/env python
from setuptools import setup

setup(
    name="tap-unity",
    version="0.1.1",
    description="Singer.io tap for extracting data",
    author="Stitch",
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
    packages=["tap_unity"],
    package_data = {
        "schemas": ["tap_unity/schemas/*.json"]
    },
    include_package_data=True,
)
