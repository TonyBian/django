#!/usr/bin/env python
# coding: utf-8

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2017-09-19 10:51

""""""

import os

output = os.popen('tasklist | findstr TitanAgent.exe')
titanagent_proc_list = output.readlines()
output.close()

output = os.popen('tasklist | findstr splunkd.exe')
splunk_proc_list = output.readlines()
output.close()

output = os.popen('tasklist | findstr zabbix_agentd.exe')
zabbix_proc_list = output.readlines()
output.close()

if len(titanagent_proc_list) > 0:
    titanagent_status = 1
else:
    titanagent_status = 0

if len(splunk_proc_list) > 0:
    splunk_status = 1
else:
    splunk_status = 0

if len(zabbix_proc_list) > 0:
    zabbix_status = 1
else:
    zabbix_status = 0

opstools_status = {
    'titanagent': titanagent_status,
    'splunk': splunk_status,
    'zabbix': zabbix_status,
}
print opstools_status
