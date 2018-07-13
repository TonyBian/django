#!/bin/bash
# coding: utf-8

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2017-09-19 11:25

salt '*' state.highstate -t 180
salt '*' saltutil.sync_all -t 180
salt '*' sys.reload_modules -t 180
