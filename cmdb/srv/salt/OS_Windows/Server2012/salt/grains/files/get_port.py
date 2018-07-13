#!/usr/bin/env python
# coding: utf-8

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2017-09-19 10:51

""""""

import subprocess

output = subprocess.Popen('netstat -ano', shell=True, stdout=subprocess.PIPE)
netstat_list = output.stdout.readlines()

task_output = subprocess.Popen('tasklist', shell=True, stdout=subprocess.PIPE)
task_list_rawdata = task_output.stdout.readlines()[3:]

task_list = []

for task in task_list_rawdata:
    task = (task.split()[0], task.split()[1])
    task_list.append(task)

tcp_port_set = set()
udp_port_set = set()

for netstat in netstat_list:
    try:
        port = int(netstat.split()[1].split(':')[-1])
    except (ValueError, IndexError):
        continue

    state = netstat.split()[-2]
    local_addr = netstat.split()[1].split(':')[0]
    port_type = netstat.split()[0]
    pid = netstat.split()[-1]

    for task in task_list:
        if pid == task[1]:
            program = task[0]

    try:
        type(program)
    except NameError:
        program = ''

    if port_type.lower() == 'tcp' and state == 'LISTENING' and local_addr == '0.0.0.0':
        tcp_port_set.add((program, port))
    elif port_type.lower() == 'udp' and local_addr == '0.0.0.0':
        udp_port_set.add((program, port))

port_dict = {'TCP': list(tcp_port_set), 'UDP': list(udp_port_set)}
print port_dict
