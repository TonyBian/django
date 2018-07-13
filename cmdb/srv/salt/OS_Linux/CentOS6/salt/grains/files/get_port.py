#!/usr/bin/env python
# coding: utf-8

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2017-09-19 10:51

""""""

import subprocess

output = subprocess.Popen('netstat -anp', shell=True, stdout=subprocess.PIPE)
netstat_list = output.stdout.readlines()
tcp_port_set = set()
udp_port_set = set()

for netstat in netstat_list:
    try:
        port = int(netstat.split()[3].split(':')[-1])
    except (ValueError, IndexError):
        continue
    try:
        program = netstat.split()[-1].split('/')[1]
    except IndexError:
        program = ''
    state = netstat.split()[-2]
    local_addr = netstat.split()[3].split(':')[0]
    port_type = netstat.split()[0]

    if port_type.lower() == 'tcp' and state == 'LISTEN' and local_addr == '0.0.0.0':
        tcp_port_set.add((program, port))
    elif port_type.lower() == 'udp' and local_addr == '0.0.0.0':
        udp_port_set.add((program, port))

port_dict = {'TCP': list(tcp_port_set), 'UDP': list(udp_port_set)}
print port_dict
