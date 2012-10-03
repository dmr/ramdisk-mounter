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


Requirements: Mac OSX 10.7.5, linux has tmpfs...

Report Bugs if you notice any.


Installation
------------

Ramdisk-Mounter can be installed via pip from this repository:

    pip install git+http://github.com/dmr/ramdisk-mounter.git#egg=ramdisk-mounter

The installation provided the command "ramdisk_mounter". Basic usage:

    mkdir ram_fold

    # create a ramdisk with 2GB
    ramdisk_mounter -f fold/ attach -s 2048

    # <do i/o heavy commands now>

    # detach RAM disk again
    ramdisk_mounter -f fold/ detach


You can run the tests by executing

    python setup.py test
