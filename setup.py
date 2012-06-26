#!/usr/bin/python

PROJECT = 'stackutils'
VERSION = '0.2'

from setuptools import setup, find_packages

from distutils.util import convert_path
from fnmatch import fnmatchcase
import os
import sys

try:
    long_description = open('README.rst', 'rt').read()
except IOError:
    long_description = ''

setup(
    name=PROJECT,
    version=VERSION,

    description='A collection of utilities for OpenStack',
    long_description=long_description,

    author='Lars Kellogg-Stedman',
    author_email='lars@seas.harvard.edu',

    install_requires=['distribute', 'cliff', 'sqlalchemy'],

    namespace_packages=[],
    packages=find_packages(),
    include_package_data=True,

    entry_points={
        'console_scripts': [
            'stackutil = stackutil.main:main'
            ],
        'stackutil.command': [
            'purge_volumes = stackutil.purge:PurgeVolumes',
            'purge_ips = stackutil.purge:PurgeIPS',
            'purge_instances = stackutil.purge:PurgeInstances',
            'purge_services = stackutil.purge:PurgeServices',
            ],
        },

    zip_safe=False,
    )

