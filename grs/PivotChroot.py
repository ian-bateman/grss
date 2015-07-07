#!/usr/bin/env python

import glob
import re
import os
import shutil

from grs.Constants import CONST
from grs.MountDirectories import MountDirectories


class PivotChroot():
    """ doc here
        more doc
    """

    def __init__(self, tmpdir = CONST.TMPDIR, portage_configroot = CONST.PORTAGE_CONFIGROOT, \
            logfile = CONST.LOGFILE):
        """ doc here
            more doc
        """
        self.tmpdir = tmpdir
        self.portage_configroot = portage_configroot
        self.logfile = logfile


    def pivot(self, subchroot, md):
        """ doc here
            more doc
        """
        some_mounted, all_mounted = md.are_mounted()
        if some_mounted:
            md.umount_all()

        # TODO: we need to move this code into its own class and inherit
        # Rotate any previous portage_configroots out of the way
        dirs = glob.glob('%s.*' % self.portage_configroot)
        indexed_dir = {}
        for d in dirs:
            m = re.search('^.+\.(\d+)$', d)
            indexed_dir[int(m.group(1))] = d
        count = list(indexed_dir.keys())
        count.sort()
        count.reverse()
        for c in count:
            current_dir = indexed_dir[c]
            m = re.search('^(.+)\.\d+$', current_dir)
            next_dir = '%s.%d' % (m.group(1), c+1)
            shutil.move(current_dir, next_dir)
        # If there is a directory, then move it to %s.0
        if os.path.isdir(self.portage_configroot):
            shutil.move(self.portage_configroot, '%s.0' % self.portage_configroot)

        inner_chroot = os.path.join(self.portage_configroot, subdir)
        shutil.move(inner_chroot, os.path.join(self.tmpdir, 'system'))

        if all_mounted:
            md.mount_all()