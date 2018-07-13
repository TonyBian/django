#!/usr/bin/env python
# coding: utf-8

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2017-09-26 14:56

""""""

import platform

systype = platform.system()


def _cmd(script):
    script_extension = script.split('.')[-1]

    if script_extension == 'py' and systype == 'Linux':
        cmd = 'python {}'.format(script)
    if script_extension == 'py' and systype == 'Windows':
        cmd = r'C:\salt\bin\python.exe {}'.format(script)
    if script_extension == 'sh':
        cmd = 'sh {}'.format(script)
    if script_extension == 'ps1':
        cmd = 'powershell -NoProfile -ExecutionPolicy Bypass -File {}'.format(script)

    return cmd
