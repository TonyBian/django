#!/usr/bin/env python
# coding: utf-8

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2017-07-27 15:11

"""
get vminfo
"""
import subprocess
import platform
from _cmd import _cmd

systype = platform.system()

if systype == 'Windows':
    def get_vminfo():
        grains = {}

        get_vmsn_script = r'c:\srv\salt\Virt_Hyper-V\salt\grains\files\get_vmsn.ps1'
        output = subprocess.Popen(
            _cmd(get_vmsn_script),
            shell=True,
            stdout=subprocess.PIPE
        )
        vmsn_format = output.stdout.read().replace('\n', '')
        grains['vmsn'] = eval(vmsn_format)

        get_vmguest_script = r'c:\srv\salt\Virt_Hyper-V\salt\grains\files\get_vmguest.ps1'
        output = subprocess.Popen(
            _cmd(get_vmguest_script),
            shell=True,
            stdout=subprocess.PIPE
        )
        vmguest_format = output.stdout.read().replace('\n', '')
        grains['vmguest'] = eval(vmguest_format)

        get_vmhost_script = r'c:\srv\salt\Virt_Hyper-V\salt\grains\files\get_vmhost.ps1'
        output = subprocess.Popen(
            _cmd(get_vmhost_script),
            shell=True,
            stdout=subprocess.PIPE
        )
        vmhost_format = output.stdout.read().replace('\n', '')
        grains['vmhost'] = eval(vmhost_format)

        return grains
