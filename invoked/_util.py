# -*- coding: utf-8 -*-
"""
Utilities
~~~~~~~~~

"""

import contextlib as _contextlib
import errno as _errno
import os as _os

from . import _settings

@_contextlib.contextmanager
def root_dir():
    """ chdir() into the root directory """
    root = _settings.env.root

    old = _os.getcwd()
    try:
        _os.chdir(root)
        yield
    finally:
        _os.chdir(old)


def rm_f(name):
    """ rm -f file """
    try:
        _os.unlink(name)
    except OSError as e:
        if e.errno != _errno.ENOENT:
            raise

