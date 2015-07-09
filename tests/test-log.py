#!/usr/bin/python

import os
import sys
sys.path.append(os.path.abspath('..'))

import hashlib
import shutil
from grs import Log

logdir = '/tmp/test-log'

def doit(lo, stamped = False):
    # Create a log with knowing contents and rotate 3 times.
    for i in range(10):
        lo.log('first %d' % i, stamped)
    lo.rotate_logs()
    lo.rotate_logs()
    lo.rotate_logs()
    for i in list(range(9,-1,-1)):
        lo.log('second %d' % i, stamped)


def hashtest(expect_pass = True):
    # Hash up our log and three rotations.  Do we get what we expected?
    m = hashlib.md5()
    for i in [ '', '.0', '.1', '.2']:
        log = os.path.join(logdir, 'test.log%s' % i)
        with open(log, 'r') as f:
            m.update(f.read().encode('ascii'))
    if expect_pass:
        assert(m.hexdigest() == '485b8bf3a9e08bd5ccfdff7e1a8fe4e1')
    else:
        assert(m.hexdigest() != '485b8bf3a9e08bd5ccfdff7e1a8fe4e1')

if __name__ == "__main__":
    if os.path.isdir(logdir):
        shutil.rmtree(logdir)
    os.makedirs(logdir)
    logfile = os.path.join(logdir, 'test.log')
    lo = Log(logfile)

    doit(lo, stamped=False)
    hashtest(expect_pass=True)
    doit(lo, stamped=True)
    hashtest(expect_pass=False)

    # Make sure we're dropping past the upper limit.
    lo.rotate_logs(upper_limit=2)
    assert(os.path.isfile(logfile))
    assert(os.path.isfile(logfile+'.0'))
    assert(os.path.isfile(logfile+'.1'))
    assert(os.path.isfile(logfile+'.2'))
    assert(not os.path.isfile(logfile+'.3'))
    assert(not os.path.isfile(logfile+'.4'))
    assert(not os.path.isfile(logfile+'.5'))
