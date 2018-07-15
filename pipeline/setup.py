#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

setup(
    name='pipeline',
    version='1.0.0',
    description='Scrapy pipeline project',
    url='https://github.com/DataRetrieval/pipeline',
    author='Ouahib El Hanchi',
    author_email='ouahib.el.hanchi@gmail.com',
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    entry_points = {'scrapy': ['settings = pipeline.settings']},
    include_package_data=True,
    install_requires=[
        'scrapy',
        'scrapy-fake-useragent',
        'boto',
        'demjson'
        'python-dateutil'
    ],
    extras_require={
        'dev': ['flake8'],
    },
)
