#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#############################################
# File Name: setup.py
# Author: IMJIE
# Email: imjie@outlook.com
# Created Time: 2020-1-29
#############################################

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fasttest", # 软件包发行名称
    version="0.0.4", # 软件包版本
    author="IMJIE", # 作者
    author_email="imjie@outlook.com", # 邮件
    keywords=('macaca','UI自动化','关键字自动化'),
    description="A keyword based UI testing framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Jodeee/fasttest",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={'fasttest/result':['resource/*']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',
)