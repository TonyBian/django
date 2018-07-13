#!/usr/bin/env python
# coding: utf-8

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2017-07-27 15:11

"""
get timezone info
"""
import subprocess
import platform
from _cmd import _cmd

systype = platform.system()


def get_timezoneinfo():
    grains = {}

    if systype == 'Linux':
        script = r'/srv/salt/OS_Linux/salt/grains/files/get_timezone.sh'
    if systype == 'Windows':
        return

    output = subprocess.Popen(
        _cmd(script),
        shell=True,
        stdout=subprocess.PIPE
    )
    data_format = output.stdout.read().replace('\n', '')

    grains['timezone'] = data_format

    return grains
