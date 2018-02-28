#!/usr/bin/env python
# vim: fileencoding=utf-8

from setuptools import find_packages, setup

setup(
    name='pybats',
    version='0.1',
    packages=find_packages(),
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov'],
    entry_points={
        'pytest11': [
            'pybats = pybats.pytest'
        ],
    },
)
