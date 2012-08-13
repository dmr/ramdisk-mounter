#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import subprocess

def check_is_same_device_as_root_fs(folder):
    return os.stat(folder).st_dev == os.stat('/').st_dev

def check_is_not_normal_harddrive(device):
    # make sure not to catch a real harddrive
    assert device != '/dev/disk0', device
    assert not device.startswith('/dev/disk0s'), device
    assert device != '/dev/disk1', device
    assert not device.startswith('/dev/disk1s'), device
    assert not ' ' in device, device
    assert not '\n' in device, device


class ramdisk(object):
    def __init__(self, folder=None, size=1024, debug=True):
        self.debug = debug

        if not folder:
            base_folder = os.path.dirname(__file__)
            folder = os.path.abspath(os.path.join(base_folder, 'tmp_folder'))
            # TODO: os.tempname?

        if not os.path.exists(folder):
            raise Exception('please pass create_folder or choose existing folder')

        assert os.path.exists(folder), 'Folder must exist!'
        self.folder = folder

        assert check_is_same_device_as_root_fs(folder), ('Folder must be on / '
                     '(ROOT) and must not be a different device (possibly '
                     'already a RAMDISK)! Maybe try "umount {0}"?').format(self.folder)
        self.attached = False

        assert isinstance(size, int), 'Please pass integer size!'
        assert size < 2048, 'ramdisks > 2GB not supported'

        # 512MB --> ram://1048576
        self.size = size * 2048 # 2048 blocksize?

    def __enter__(self):
        create_ramdisk_stdout = subprocess.check_output(['hdid','-nomount',
                                          'ram://{0}'.format(self.size)])
        self.ram_disk_device = create_ramdisk_stdout.strip().strip('\n')
        check_is_not_normal_harddrive(self.ram_disk_device)
        if self.debug: print 'Created RAM disk', self.ram_disk_device

        if self.debug: print 'Formatting RAM disk', self.ram_disk_device
        format_stdout = subprocess.check_output(['newfs_hfs',self.ram_disk_device])
        assert format_stdout, format_stdout #Initialized /dev/rdisk13 as a 512 MB HFS Plus volume

        old_ionode_nbr = os.stat(self.folder).st_ino

        if self.debug: print 'Mounting RAM disk', self.ram_disk_device, 'as', self.folder
        _mount_ret_code = subprocess.check_call(['mount','-t','hfs',
                                                 self.ram_disk_device,
                                                 self.folder])

        if self.debug: print 'RAM disk',self.ram_disk_device,'mounted as',self.folder

        assert old_ionode_nbr != os.stat(self.folder).st_ino
        # TODO: probably remove this
        assert not check_is_same_device_as_root_fs(self.folder)

        self.attached = True
        return self.folder

    def __exit__(self, type, value, traceback):
        if not self.attached:
            if self.debug: print "no RAM disk to detach --> Exiting"
            return

        if self.debug: print 'Umount folder',self.folder
        _umount_ret_code = subprocess.check_call(['umount',self.folder])

        if self.debug: print 'Detaching RAM disk',self.ram_disk_device
        detach_ramdisk_stdout = subprocess.check_output(['hdiutil','detach',
                                            self.ram_disk_device])
        assert detach_ramdisk_stdout, detach_ramdisk_stdout #"disk15" ejected.

        # from outer function
        if type:
            if self.debug:
                print type, value, traceback
            if issubclass(type, Exception):
                raise
