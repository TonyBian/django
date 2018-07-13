#!/usr/bin/env python
# coding: utf-8

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2017-09-08 14:15

"""get grains"""

import salt.client

TIMEOUT = 300


def get_vmhost_grains():
    # get vmhost grains
    local = salt.client.LocalClient()
    vmhosts = local.cmd(
        'productname:^((?!Virtual Machine).)*$',
        'grains.items',
        timeout=TIMEOUT,
        expr_form='grain_pcre',
    )
    return vmhosts


def get_vmguest_grains():
    # get vmguest grains
    local = salt.client.LocalClient()
    vmguests = local.cmd(
        'productname:Virtual Machine',
        'grains.items',
        timeout=TIMEOUT,
        expr_form='grain',
    )
    return vmguests


def get_all_grains():
    # get all grains
    local = salt.client.LocalClient()
    all_grains = local.cmd('*', 'grains.items', timeout=TIMEOUT)
    return all_grains
