#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

import sys
assert sys.platform.startswith('darwin'), 'This package is for mac only.'

setup(
    name='Ramdisk-Mounter',
    version='0.1.1',
    url='https://github.com/dmr/ramdisk-mounter',
    license='MIT',
    author='Daniel Rech',
    author_email='danielmrech@gmail.com',
    description='',
    long_description=__doc__,
    py_modules= ['ramdisk_mounter'],

    entry_points={
        'console_scripts': [
            'ramdisk_mounter = ramdisk_mounter:main',
            ],
        },

    install_requires=[
        'argparse',
        'subprocess32'
    ],
    zip_safe=False,
    platforms='darwin',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        ],

    tests_require=['spec'],
)
