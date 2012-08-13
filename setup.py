#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Ramdisk-Mounter
---------------

A demonstration how to create a Ramdisk on Mac OSX (highly experimental!).

This can be very useful if a fast temporary storage is needed.
Provides a with definition that can be used like this:

    fold = "testfolder"
    assert check_is_same_device_as_root_fs(fold)
    with ramdisk_mounter.ramdisk(folder=fold):
        assert not check_is_same_device_as_root_fs(fold)
    assert check_is_same_device_as_root_fs(fold)


Requirements: Mac OSX 10.7.2 because "hdid", "newfs_hfs", "hdiutil" are used.
Feel free tp port to other platforms or contribute Bugs!
"""

from setuptools import setup

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
    scripts=['ramdisk_mounter.py'],
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        ],

    tests_require=['Attest'],
    test_loader='attest:auto_reporter.test_loader',
    test_suite='tests.ramdisk_test'
)