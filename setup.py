#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Setup script for hiiguid."""

from setuptools import setup, find_packages

from pylogd import VERSION
version = '.'.join(map(str, VERSION))

# some trove classifiers:

# License :: OSI Approved :: MIT License
# Intended Audience :: Developers
# Operating System :: POSIX

setup(
    name='hiiguid',
    version=version,
    description="HiiGUID generator",
    long_description=open('README.md').read(),
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
    ],
    keywords='guid uuid',
    author='HiiDef',
    author_email='support@hiidef.com',
    url="'http://github.com/hiidef/hiiguid'",
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite="tests",
    # -*- Extra requirements: -*-
    install_requires=[
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)
