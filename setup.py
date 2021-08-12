#!/usr/bin/python
# -*- coding=utf-8 -*-
# to install type:
# python setup.py install --root=/

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="mishkal",
    version="1.10",
    author="Taha Zerrouki",
    author_email="taha.zerrouki@gmail.com",
    description="Mishkal: Arabic text diacritization library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/linuxscout/mishkal",
    project_urls={
        "sourceforge mishkal": "http://mishkal.sourceforge.net/",
        "Bug Tracker": "https://github.com/linuxscout/mishkal/issues",
    },
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: GPL-3.0",
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Operating System :: OS Independent",
    ],
    license="GPL-3.0",
    package_dir={"mishkal": "mishkal"},
    packages=["mishkal"],
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "mishkal": ["doc/*.*", "doc/html/*", "data/*.sqlite", "data/*.sql"],
    },
)
