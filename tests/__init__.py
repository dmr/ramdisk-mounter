#!/usr/bin/env python
# -*- coding: utf-8 -*-
from attest import Tests

ramdisk_test = Tests()


@ramdisk_test.test
def test_is_installed():
    import ramdisk_mounter
    assert True


import os
import tempfile

fold = tempfile.gettempdir()

import ramdisk_mounter


@ramdisk_test.test
def test_error_inside_with_is_raised():
    # raising error still umounts the ramdisk
    def fct_with_error_n_ramdisk():
        with ramdisk_mounter.ramdisk(fold) as tmp_folder:
            assert not ramdisk_mounter.check_is_same_device_as_root_fs(tmp_folder)
            assert 0
    try:
        fct_with_error_n_ramdisk()
        raise ValueError("This should not happen")
    except AssertionError:
        # variable name used outside with <-- wrong, kind of
        print


@ramdisk_test.test
def test_tmpfs_doesnt_exist_outside_with_and_unicode_name_possible():
    tmp_file = os.path.join(fold, 'temporary_file.txt')
    with ramdisk_mounter.ramdisk(fold):
        with open(tmp_file, 'w') as f:
            f.write('test')
        assert os.path.exists(tmp_file)
    assert not os.path.exists(tmp_file)


if __name__ == '__main__':
    csp_test.run()