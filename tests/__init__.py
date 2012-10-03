#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

import string, random
import time
import os

import ramdisk_mounter

fold = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '_folder_of_ram_disk')
)
if not os.path.exists(fold):
    os.makedirs(fold)


class TestRaiseErrorToOuterContext(unittest.TestCase):
    def test_error_inside_with_is_raised(self):
        # raising error still umounts the ramdisk
        def fct_with_error_n_ramdisk():
            with ramdisk_mounter.Ramdisk(
                folder=fold,
                size=128
            ) as tmp_folder:
                assert not ramdisk_mounter.check_is_same_device_as_root_fs(tmp_folder)
                assert 0

        self.assertRaises(
            AssertionError, # raised inside the ramdisk operation
            fct_with_error_n_ramdisk
        )


def test_tmpfs_doesnt_exist_outside_with_and_unicode_name_possible():
    tmp_file = os.path.join(fold, 'temporary_file.txt')
    with ramdisk_mounter.Ramdisk(
        folder=fold,
        size=128
    ):
        with open(tmp_file, 'w') as f:
            f.write('test')
        assert os.path.exists(tmp_file)
    assert not os.path.exists(tmp_file)


def test_compare_speed():
    tmp_file = os.path.join(fold, 'temporary_file_compare_speed.txt')

    r_word = lambda length: "".join(
        [random.choice(string.letters) for _ in range(length)])

    text = " ".join([r_word(5) for _ in range(1000000)])

    #import sys
    #print sys.getsizeof(text)

    before = time.time()
    with open(tmp_file, 'w') as fp:
        fp.write(text)
    speed_without_ramdisk = time.time() - before

    with ramdisk_mounter.Ramdisk(
        folder=fold,
        size=128
    ):
        before = time.time()
        with open(tmp_file, 'w') as fp:
            fp.write(text)
        speed_with_ramdisk = time.time() - before

    assert speed_with_ramdisk < speed_without_ramdisk

    print "Without RAMDISK: %s\n--> With RAMDISK: %s" % (
        speed_without_ramdisk, speed_with_ramdisk)
    #get_file_size = lambda file_name: os.stat(file_name).st_size
    #print get_file_size(tmp_file)
test_compare_speed.__test__ = False
