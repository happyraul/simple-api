# -*- encoding: utf-8 -*-
"""
Invoke task lookup
~~~~~~~~~~~~~~~~~~
See all available tasks using `inv[oke] -l`.
Add new task module to invoked/__init__.
"""

# pylint: disable =  invalid-name


def namespace():
    """ Create configured namespace """
    import sys as _sys
    import os as _os
    _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))

    import invoke as _invoke
    from invoked import _settings
    import invoked

    result = _invoke.Collection(*[value for key, value in vars(invoked).items() 
                                  if not key.startswith('__')])
    result.configure(_settings.env)
    return result

namespace = namespace()

