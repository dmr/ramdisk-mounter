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


Installation
------------

Ramdisk-Mounter can be installed via pip from this repository. It's not on Pypi yet because it only supports Mac OS X and is still only a development version.

    1. Clone this repository && cd ramdisk-mounter
    2. python setup.py test
    3. python setup.py develop
