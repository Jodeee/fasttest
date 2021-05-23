#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#############################################
# File Name: setup.py
# Author: IMJIE
# Email: imjie@outlook.com
# Created Time: 2020-1-29
#############################################

import sys
import setuptools

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

info = sys.version_info
if info.major == 3 and info.minor <= 7:
    requires = [
        'PyYAML>=5.1.2',
        'wd>=1.0.1',
        'selenium',
        'colorama',
        'opencv-contrib-python==3.4.2.16'
    ]
else:
    requires = [
        'PyYAML>=5.1.2',
        'wd>=1.0.1',
        'selenium',
        'colorama',
        'opencv-contrib-python'
    ]
setuptools.setup(
    name="fasttest",
    version="1.0.1",
    author="IMJIE",
    author_email="imjie@outlook.com",
    keywords=('macaca', 'appium', 'selenium', 'APP自动化', 'WEB自动化', '关键字驱动'),
    description="关键字驱动自动化框架",
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
    install_requires=requires,
    entry_points={
        'console_scripts':[
            'fasttest = fasttest.fasttest_runner:main'
        ]
    }
)