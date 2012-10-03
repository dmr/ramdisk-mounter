#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import logging

import argparse
import subprocess32 as subprocess


logger = logging.getLogger("ramdisk_mounter")


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


class Ramdisk(object):
    attached = False
    def __init__(self, folder, size=None):
        self.folder = clean_folder(folder)

        # TODO: pass to attach?
        if size:
            # 512MB --> ram://1048576
            self.size = clean_ram_disk_size(size) * 2048 # 2048 blocksize?

    def __enter__(self):
        self.attach()
        return self.folder

    def __exit__(self, type, value, traceback):
        self.detach()

        # from outer function
        if type:
            if issubclass(type, Exception):
                raise

    def attach(self):
        if self.attached:
            raise Exception("Wrong usage. Ramdisk should not be attached")

        if not check_is_same_device_as_root_fs(self.folder):
            msg = ('Folder must be on / '
                   '(ROOT) and must not be a different device (possibly '
                   'already a RAMDISK)! Maybe try "umount {0}"?').format(self.folder)
            raise argparse.ArgumentTypeError(msg)

        create_ramdisk_stdout = subprocess.check_output(
            ['hdid','-nomount', 'ram://{0}'.format(self.size)])
        ram_disk_device = create_ramdisk_stdout.strip().strip('\n')
        check_is_not_normal_harddrive(ram_disk_device)
        logger.info('Created RAM disk {0}'.format(ram_disk_device))

        logger.info('Formatting RAM disk...')
        format_stdout = subprocess.check_output(['newfs_hfs', ram_disk_device])
        #Initialized /dev/rdisk13 as a 512 MB HFS Plus volume
        assert format_stdout, format_stdout

        old_ionode_nbr = os.stat(self.folder).st_ino

        logger.info('Mounting RAM disk {0} as {1}'.format(ram_disk_device, self.folder))
        subprocess.check_call(['mount','-t','hfs', ram_disk_device, self.folder])

        assert old_ionode_nbr != os.stat(self.folder).st_ino

        # TODO: probably remove this
        assert not check_is_same_device_as_root_fs(self.folder)

        self.ram_disk_device = ram_disk_device
        self.attached = True

    def detach(self):
        if not self.attached:
            assert not check_is_same_device_as_root_fs(self.folder), "Not a ramdisk."
            logger.info("{0} might be a RAM disk. Umounting...".format(self.folder))

        logger.info('Umount folder {0}'.format(self.folder))
        # Changed behavior since 10.7.4: --> use diskutil u(n)mountDisk
        # subprocess.check_call(['diskutil','umountDisk',self.folder])
        # Re-Changed again 10.7.5 --> umount
        subprocess.check_call(['umount', self.folder])

        if hasattr(self, 'ram_disk_device'):
            logger.info('Detaching RAM disk')
            detach_ramdisk_stdout = subprocess.check_output(
                ['hdiutil','detach', self.ram_disk_device]
            )
            assert detach_ramdisk_stdout, detach_ramdisk_stdout #"disk15" ejected.
        else:
            logger.info("I didn't create the RAM disk --> please execute "
                   "'hdutil detach your_device_here' manually")
            # will be done automatically??? on 10.7.5 yes.
        self.attached = False


def clean_folder(dir_name):
    msg = "Directory does not exist: {0}".format(dir_name)
    if not dir_name:
        raise argparse.ArgumentTypeError(msg)
    if not os.path.exists(dir_name):
        raise argparse.ArgumentTypeError(msg)
    if not os.path.isdir(dir_name):
        raise argparse.ArgumentTypeError(msg)
    return os.path.abspath(dir_name)


def clean_ram_disk_size(size):
    return int(size)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder',
        type=clean_folder, help="Folder where RAM disk will be mounted",
        required=True
    )
    subparsers = parser.add_subparsers()
    parser_a = subparsers.add_parser('attach', help='Attach it')
    parser_a.set_defaults(func_name='attach')
    parser_a.add_argument('-s','--size',
        help="Size in MB", default=1024,
        type=clean_ram_disk_size
    )
    parser_d = subparsers.add_parser('detach', help='Detach it')
    parser_d.set_defaults(func_name='detach')

    parsed_args = parser.parse_args()

    if parsed_args.func_name == "attach":
        if parsed_args.size > 2048:
            while True:
                is_sure = raw_input(
                    'Your RAM disk will be huge. '
                    'This might cause problems if the operation system '
                    'might need the memory. Continue? (yes/no) ')
                if is_sure.lower() == "no":
                    import sys
                    print "Exiting."
                    sys.exit(1)
                if is_sure.lower() == "yes":
                    break

        Ramdisk(folder=parsed_args.folder,
            size=parsed_args.size
        ).attach()
    else:
        Ramdisk(folder=parsed_args.folder).detach()
