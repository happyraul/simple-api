# -*- coding: utf-8 -*-
"""
Docker tasks
~~~~~~~~~~~~
"""

import shutil as _shutil

import invoke as _invoke

from . import _util


@_invoke.task()
def build(ctx):
    
    with _util.root_dir():
        _shutil.copytree('app', 'docker/dist/app', ignore=lambda *args: ('__pycache__',))
        _shutil.copy('requirements.txt', 'docker/dist')
        _shutil.copy('manage.py', 'docker/dist')

        try:
            ctx.run('docker build -f docker/Dockerfile -t simple-api:latest .', echo=True)
        except:
            pass
        finally:
            _shutil.rmtree('docker/dist')

