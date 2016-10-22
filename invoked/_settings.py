# -*- coding: utf-8 -*-
"""
Invoke settings
~~~~~~~~~~~~~~~

"""

import os as _os


class adict(dict):
    """ small and hacky attrdict implementation """

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

env = adict(
    root=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
)

