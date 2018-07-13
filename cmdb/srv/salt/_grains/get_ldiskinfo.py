#!/usr/bin/env python
# coding: utf-8

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2017-07-27 15:11

"""
get ldisk info
"""
import subprocess
import platform
from _cmd import _cmd

systype = platform.system()


def get_ldiskinfo():
    grains = {}

    if systype == 'Windows':
        script = r'c:\srv\salt\OS_Windows\salt\grains\files\get_ldisk.ps1'
    if systype == 'Linux':
        return

    output = subprocess.Popen(
        _cmd(script),
        shell=True,
        stdout=subprocess.PIPE
    )
    data_format = output.stdout.read().replace('\n', '')

    grains['ldisk'] = eval(data_format)

    return grains
