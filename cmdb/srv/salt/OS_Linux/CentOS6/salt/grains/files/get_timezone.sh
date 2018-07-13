#!/bin/bash
# coding: utf-8

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2017-09-15 14:18

arg1=`date +'%Z%:z'`
arg2=`cat /etc/sysconfig/clock | grep ZONE | awk -F '=' '{print $2}' | awk -F '"' '{print $2}'`

timezone=($arg1)$arg2

echo $timezone
