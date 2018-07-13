#!/usr/bin/env python2.7
# coding: utf-8

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2017-09-07 15:35

"""cmdb main script"""

from __future__ import unicode_literals
import init
import traceback
import django
import re
import json
import copy
from django.utils import timezone
from public.setup_django import setup_django
from public.get_grains import get_vmhost_grains
from public.get_grains import get_vmguest_grains
from cmdb.modules.get_fields_dict import get_fields_dict
from cmdb.modules.try_update import try_update
from cmdb.models import Grains_Vmhost
from cmdb.models import Grains_Vmsn
from cmdb.models import Grains_Vmguest
from cmdb.models import Grains_HostChgHistory
from cmdb.models import Grains_HostGeneral
from cmdb.models import Grains_HostHw
from cmdb.models import Grains_HostDns
from cmdb.models import Grains_HostNICs
from cmdb.models import Grains_HostSaltInfo
from cmdb.models import Grains_GuestChgHistory
from cmdb.models import Grains_GuestGeneral
from cmdb.models import Grains_GuestHw
from cmdb.models import Grains_GuestDns
from cmdb.models import Grains_GuestNICs
from cmdb.models import Grains_GuestSaltInfo
from cmdb.models import Grains_Exception

setup_django()

vmhosts_rawdata = get_vmhost_grains()
vmguests_rawdata = get_vmguest_grains()

# clear Grains_Exception
Grains_Exception.objects.all().delete()

capture_date = timezone.now()
for hostname, v in vmhosts_rawdata.iteritems():
    if v is False:
        exception = {
            'localhost': hostname,
            'SerialNumber': v,
            'errmsg': "getting grains failure!",
            'tracebackmsg': '',
            'capture_date': capture_date,
        }

        Grains_Exception.objects.create(**exception)

for hostname, v in vmguests_rawdata.iteritems():
    if v is False:
        exception = {
            'localhost': hostname,
            'SerialNumber': v,
            'errmsg': "getting grains failure!",
            'tracebackmsg': '',
            'capture_date': capture_date,
        }

        Grains_Exception.objects.create(**exception)

vmhosts = {k: v for k, v in vmhosts_rawdata.iteritems() if v is not False}
for hostname in vmhosts.iterkeys():
    vmhosts_timezone = vmhosts[hostname]['timezone'].decode('utf-8')
    vmhosts[hostname]['timezone'] = vmhosts_timezone

    nic_rawdata = copy.deepcopy(vmhosts[hostname]['hwaddr_interfaces'])
    for nic_name, nic_value in nic_rawdata.iteritems():
        vmhosts[hostname]['hwaddr_interfaces'].pop(nic_name)
        nic_name = nic_name.decode('utf-8')
        vmhosts[hostname]['hwaddr_interfaces'].update({nic_name: nic_value})

    ipv4_rawdata = copy.deepcopy(vmhosts[hostname]['ip4_interfaces'])
    for nic_name, nic_value in ipv4_rawdata.iteritems():
        vmhosts[hostname]['ip4_interfaces'].pop(nic_name)
        nic_name = nic_name.decode('utf-8')
        vmhosts[hostname]['ip4_interfaces'].update({nic_name: nic_value})

    ipv6_rawdata = copy.deepcopy(vmhosts[hostname]['ip6_interfaces'])
    for nic_name, nic_value in ipv6_rawdata.iteritems():
        vmhosts[hostname]['ip6_interfaces'].pop(nic_name)
        nic_name = nic_name.decode('utf-8')
        vmhosts[hostname]['ip6_interfaces'].update({nic_name: nic_value})

    dns_rawdata = copy.deepcopy(vmhosts[hostname]['nameservers'])
    for key, value in dns_rawdata.iteritems():
        vmhosts[hostname]['nameservers'].pop(key)
        key = key.decode('utf-8')
        vmhosts[hostname]['nameservers'].update({key: value})

    if 'vmhost' in vmhosts[hostname].keys():
        if not vmhosts[hostname]['vmhost'].keys()[0]:
            vmhosts[hostname].pop('vmhost')
            vmhosts[hostname].pop('vmguest')
            vmhosts[hostname].pop('vmsn')

    if 'vmguest' in vmhosts[hostname].keys():
        for vm_id in vmhosts[hostname]['vmguest']:
            Notes_rawdata = vmhosts[hostname]['vmguest'][vm_id]['Notes'].decode(
                'utf-8')
            notes_r = re.compile(r'#CLUSTER-INVARIANT#:{.{36}}')
            Notes = notes_r.sub('', Notes_rawdata).strip()
            vmhosts[hostname]['vmguest'][vm_id]['Notes'] = Notes
            Path = vmhosts[hostname]['vmguest'][vm_id]['Path'].replace(
                '\x0b', '\\v').replace('\x08', '\\b').replace('\x07', '\\a')
            vmhosts[hostname]['vmguest'][vm_id]['Path'] = Path

vmguests = {k: v for k, v in vmguests_rawdata.iteritems() if v is not False}
for hostname in vmguests.iterkeys():
    vmguests_timezone = vmguests[hostname]['timezone'].decode('utf-8')
    vmguests[hostname]['timezone'] = vmguests_timezone

    nic_rawdata = vmguests[hostname]['hwaddr_interfaces']
    ipv4_rawdata = vmguests[hostname]['ip4_interfaces']
    ipv6_rawdata = vmguests[hostname]['ip6_interfaces']
    for i in (nic_rawdata, ipv4_rawdata, ipv6_rawdata):
        try:
            i.pop('lo')
        except KeyError:
            pass

    nic_rawdata = copy.deepcopy(nic_rawdata)
    ipv4_rawdata = copy.deepcopy(ipv4_rawdata)
    ipv6_rawdata = copy.deepcopy(ipv6_rawdata)

    for nic_name, nic_value in nic_rawdata.iteritems():
        vmguests[hostname]['hwaddr_interfaces'].pop(nic_name)
        nic_name = nic_name.decode('utf-8')
        vmguests[hostname]['hwaddr_interfaces'].update({nic_name: nic_value})

    for nic_name, nic_value in ipv4_rawdata.iteritems():
        vmguests[hostname]['ip4_interfaces'].pop(nic_name)
        nic_name = nic_name.decode('utf-8')
        vmguests[hostname]['ip4_interfaces'].update({nic_name: nic_value})

    for nic_name, nic_value in ipv6_rawdata.iteritems():
        vmguests[hostname]['ip6_interfaces'].pop(nic_name)
        nic_name = nic_name.decode('utf-8')
        vmguests[hostname]['ip6_interfaces'].update({nic_name: nic_value})

    if vmguests[hostname]['os'] == 'Windows':
        dns_rawdata = copy.deepcopy(vmguests[hostname]['nameservers'])
        for key, value in dns_rawdata.iteritems():
            vmguests[hostname]['nameservers'].pop(key)
            key = key.decode('utf-8')
            vmguests[hostname]['nameservers'].update({key: value})

all_grains = {'all_grains': [{'host': vmhosts}, {'guest': vmguests}]}

with open('/tmp/all_grains.txt', 'w') as grains_file:
    grains_file.write(json.dumps(all_grains))

# Grains_Vmhost
vmhost_sn_list = []
for hostname in vmhosts.iterkeys():
    # get special field's value
    SerialNumber = vmhosts[hostname]['serialnumber'].strip().strip('.')

    if 'vmhost' in vmhosts[hostname].keys():
        ComputerName = vmhosts[hostname]['vmhost'].keys()[0]
        MemoryCapacity_rawdata = vmhosts[hostname]['vmhost'][ComputerName]['MemoryCapacity']
        MemoryCapacity = int(
            round(int(MemoryCapacity_rawdata) / 1024 / 1024 / 1024.0))
        rawdata_dict = vmhosts[hostname]['vmhost'][ComputerName]
    else:
        MemoryCapacity = int(round(vmhosts[hostname]['mem_total'] / 1024.0))
        rawdata_dict = {}
        ComputerName = vmhosts[hostname]['host']

    osfullname = vmhosts[hostname]['osfullname']

    hwaddr_rawdata = vmhosts[hostname]['hwaddr_interfaces']
    hwaddr_list = []
    for value in hwaddr_rawdata.itervalues():
        hwaddr_list.append(value)
    hwaddr = unicode(hwaddr_list)

    ipv4_rawdata = vmhosts[hostname]['ip4_interfaces']
    ipv4_list = []
    for value in ipv4_rawdata.itervalues():
        ipv4_list.append(value)
    ipv4 = unicode(ipv4_list)

    admin = vmhosts[hostname]['admin']

    titanagent = vmhosts[hostname]['opstools_status']['titanagent']
    splunk = vmhosts[hostname]['opstools_status']['splunk']
    zabbix = vmhosts[hostname]['opstools_status']['zabbix']

    # get vmhost sn list
    vmhost_sn_list.append(SerialNumber)

    # initialize fields dict
    vmhost_init = {
        'SerialNumber': SerialNumber,
        'ComputerName': ComputerName,
        'osfullname': osfullname,
        'MemoryCapacity': MemoryCapacity,
        'hwaddr': hwaddr,
        'ipv4': ipv4,
        'admin': admin,
        'titanagent': titanagent,
        'splunk': splunk,
        'zabbix': zabbix,
    }

    # initialize variables of function get_fields_dict()
    exclude_fields_set = {
        'SerialNumber',
        'ComputerName',
        'osfullname',
        'MemoryCapacity',
        'hwaddr',
        'ipv4',
        'admin',
        'titanagent',
        'splunk',
        'zabbix',
        'IsExpired',
        'ExpiredDate',
    }

    # call function get_fields_dict()
    vmhost = get_fields_dict(
        'Grains_Vmhost',
        exclude_fields_set,
        rawdata_dict,
        vmhost_init
    )

    offlog_fields_set = {'titanagent', 'splunk', 'zabbix'}

    # main database operation
    # initialize variables of function try_update()
    filter_dict = {'SerialNumber': SerialNumber}

    # call function try_update()
    try_update(
        SerialNumber,
        eval('Grains_Vmhost'),
        eval('Grains_HostChgHistory'),
        vmhost,
        filter_dict,
        offlog_fields_set,
    )

# get vmhost sn history list
vmhost_sn_history_list = []
for sn in Grains_Vmhost.objects.values_list('SerialNumber'):
    vmhost_sn_history_list.append(sn[0])

# Determine whether vmhost is valid
for sn in vmhost_sn_history_list:
    value = Grains_Vmhost.objects.get(SerialNumber=sn)
    value_filter = Grains_Vmhost.objects.filter(SerialNumber=sn)
    if sn not in vmhost_sn_list and value.IsExpired == 0:
        value_filter.update(IsExpired=1, ExpiredDate=unicode(timezone.now()))
    elif sn in vmhost_sn_list:
        value_filter.update(IsExpired=0)

# Grains_Vmsn
for hostname in vmhosts.iterkeys():
    # get vmsn fields list
    if 'vmsn' in vmhosts[hostname].keys():
        vmsn_list = vmhosts[hostname]['vmsn'].values()
        for i in xrange(len(vmsn_list)):
            vmsn = vmsn_list[i]
            BIOSSerialNumber = vmsn['BIOSSerialNumber']

            for hostname in vmguests.iterkeys():
                SerialNumber = vmguests[hostname]['serialnumber'].strip()
                if BIOSSerialNumber == SerialNumber:
                    osfullname = vmguests[hostname]['osfullname']
                    osrelease = vmguests[hostname]['osrelease']

                    hwaddr_rawdata = vmguests[hostname]['hwaddr_interfaces']
                    hwaddr_list = []
                    for value in hwaddr_rawdata.itervalues():
                        hwaddr_list.append(value)
                    hwaddr = unicode(hwaddr_list)

                    ipv4_rawdata = vmguests[hostname]['ip4_interfaces']
                    ipv4_list = []
                    for value in ipv4_rawdata.itervalues():
                        ipv4_list.append(value)
                    ipv4 = unicode(ipv4_list)

                    titanagent = vmguests[hostname]['opstools_status']['titanagent']
                    splunk = vmguests[hostname]['opstools_status']['splunk']
                    zabbix = vmguests[hostname]['opstools_status']['zabbix']

                    vmsn.update(
                        {'osfullname': osfullname,
                         'osrelease': osrelease,
                         'hwaddr': hwaddr,
                         'ipv4': ipv4,
                         'titanagent': titanagent,
                         'splunk': splunk,
                         'zabbix': zabbix,
                         }
                    )

            offlog_fields_set = {'titanagent', 'splunk', 'zabbix'}

            # main database operation
            # initialize variables of function try_update()
            filter_dict = {'BIOSSerialNumber': BIOSSerialNumber}

            # call function try_update()
            try_update(
                BIOSSerialNumber,
                eval('Grains_Vmsn'),
                eval('Grains_GuestChgHistory'),
                vmsn,
                filter_dict,
                offlog_fields_set,
            )

sn_list = []
for hostname in vmguests.iterkeys():
    vmsn = vmguests[hostname]['serialnumber']
    sn_list.append(vmsn)

sn_history_list = []
for sn_tuple in Grains_Vmsn.objects.values_list('BIOSSerialNumber'):
    sn_history_list.append(sn_tuple[0])

for sn in sn_history_list:
    value = Grains_Vmsn.objects.get(BIOSSerialNumber=sn)
    value_filter = Grains_Vmsn.objects.filter(BIOSSerialNumber=sn)
    if sn not in sn_list and value.IsExpired == 0:
        value_filter.update(IsExpired=1, ExpiredDate=unicode(timezone.now()))
    elif sn in sn_list:
        value_filter.update(IsExpired=0)

# Grains_Vmguest
# delete all data
Grains_Vmguest.objects.all().delete()

# insert the latest data
for hostname in vmhosts.iterkeys():
    # get special field's value
    HostSerialNumber = vmhosts[hostname]['serialnumber'].strip()

    if 'vmguest' in vmhosts[hostname].keys():
        for vm_id in vmhosts[hostname]['vmguest']:
            CreationTime_rawdata = vmhosts[hostname]['vmguest'][vm_id]['CreationTime']
            CreationTime = ('{0}{1}{2}{3}').format(
                CreationTime_rawdata[6:10],
                '/',
                CreationTime_rawdata[:5],
                CreationTime_rawdata[-9:],
            ).replace('/', '-')
            MemoryAssigned_rawdata = vmhosts[hostname]['vmguest'][vm_id]['MemoryAssigned']
            MemoryAssigned = round(
                int(MemoryAssigned_rawdata) / 1024 / 1024 / 1024.0, 2)

            MemoryStartup_rawdata = vmhosts[hostname]['vmguest'][vm_id]['MemoryStartup']
            MemoryStartup = round(
                int(MemoryStartup_rawdata) / 1024 / 1024 / 1024.0, 2)

            Notes = vmhosts[hostname]['vmguest'][vm_id]['Notes'][:100]

            # initialize fields dict
            vmguest_init = {
                'HostSerialNumber_id': HostSerialNumber,
                'VirtualSystemIdentifier_id': vm_id.upper(),
                'CreationTime': CreationTime,
                'MemoryAssigned': MemoryAssigned,
                'MemoryStartup': MemoryStartup,
                'Notes': Notes,
            }

            # initialize variables of function get_fields_dict()
            exclude_fields_set = {
                'id',
                'VirtualSystemIdentifier',
                'HostSerialNumber',
                'CreationTime',
                'MemoryAssigned',
                'MemoryStartup',
                'Notes',
            }

            rawdata_dict = vmhosts[hostname]['vmguest'][vm_id]

            # call function get_fields_dict()
            vmguest = get_fields_dict(
                'Grains_Vmguest',
                exclude_fields_set,
                rawdata_dict,
                vmguest_init
            )

            # main database operation
            Grains_Vmguest.objects.create(**vmguest)

# Grains_HostGeneral
for hostname in vmhosts.iterkeys():
    # get special field's value
    SerialNumber = vmhosts[hostname]['serialnumber'].strip()
    defaultencoding = vmhosts[hostname]['locale_info']['defaultencoding']
    defaultlanguage = vmhosts[hostname]['locale_info']['defaultlanguage']
    detectedencoding = vmhosts[hostname]['locale_info']['detectedencoding']
    osrelease_info = unicode(vmhosts[hostname]['osrelease_info'])
    path = vmhosts[hostname]['path'][:500]

    # initialize fields dict
    host_general_init = {
        'SerialNumber_id': SerialNumber,
        'defaultencoding': defaultencoding,
        'defaultlanguage': defaultlanguage,
        'detectedencoding': detectedencoding,
        'osrelease_info': osrelease_info,
        'path': path,
    }

    # initialize variables of function get_fields_dict()
    exclude_fields_set = {
        'SerialNumber',
        'defaultencoding',
        'defaultlanguage',
        'detectedencoding',
        'osrelease_info',
        'path',
    }

    rawdata_dict = vmhosts[hostname]

    # call function get_fields_dict()
    host_general = get_fields_dict(
        'Grains_HostGeneral',
        exclude_fields_set,
        rawdata_dict,
        host_general_init
    )

    # main database operation
    # initialize variables of function try_update()
    filter_dict = {'SerialNumber': SerialNumber}

    # call function try_update()
    try_update(
        SerialNumber,
        eval('Grains_HostGeneral'),
        eval('Grains_HostChgHistory'),
        host_general,
        filter_dict
    )

# Grains_HostHw
for hostname in vmhosts.iterkeys():
    # get special field's value
    SerialNumber = vmhosts[hostname]['serialnumber'].strip()
    mem_total = int(round(vmhosts[hostname]['mem_total'] / 1024.0))

    ldisk_rawdata = vmhosts[hostname]['ldisk']
    ldisk_size = {}
    for disk in ldisk_rawdata.iterkeys():
        if ldisk_rawdata[disk]['Size'].isdigit():
            size = int(
                round(int(ldisk_rawdata[disk]['Size']) / 1024 / 1024 / 1024.0))
        else:
            size = ''
        ldisk_size.update({disk: size})
    ldisk_free = {}
    for disk in ldisk_rawdata.iterkeys():
        if ldisk_rawdata[disk]['FreeSpace'].isdigit():
            free = int(
                round(int(ldisk_rawdata[disk]['FreeSpace']) / 1024 / 1024 / 1024.0))
        else:
            free = ''
        ldisk_free.update({disk: free})

    ldisk_size = unicode(ldisk_size)
    ldisk_free = unicode(ldisk_free)

    # initialize fields dict
    hosthw_init = {
        'SerialNumber_id': SerialNumber,
        'mem_total': mem_total,
        'ldisk_size': ldisk_size,
        'ldisk_free': ldisk_free,
    }

    # initialize variables of function get_fields_dict()
    exclude_fields_set = {
        'SerialNumber',
        'mem_total',
        'ldisk_size',
        'ldisk_free',
    }

    rawdata_dict = vmhosts[hostname]

    # call function get_fields_dict()
    hosthw = get_fields_dict(
        'Grains_HostHw',
        exclude_fields_set,
        rawdata_dict,
        hosthw_init
    )

    offlog_fields_set = {'ldisk_free'}

    # main database operation
    # initialize variables of function try_update()
    filter_dict = {'SerialNumber': SerialNumber}

    # call function try_update()
    try_update(
        SerialNumber,
        eval('Grains_HostHw'),
        eval('Grains_HostChgHistory'),
        hosthw,
        filter_dict,
        offlog_fields_set,
    )

# Grains_HostDns
for hostname in vmhosts.iterkeys():
    # get special field's value
    SerialNumber = vmhosts[hostname]['serialnumber'].strip()
    nameservers = unicode(vmhosts[hostname]['nameservers'])

    # initialize fields dict
    hostdns_init = {
        'SerialNumber_id': SerialNumber,
        'nameservers': nameservers,
    }

    # initialize variables of function get_fields_dict()
    exclude_fields_set = {
        'SerialNumber',
        'nameservers',
    }

    rawdata_dict = vmhosts[hostname]

    # call function get_fields_dict()
    hostdns = get_fields_dict(
        'Grains_HostDns',
        exclude_fields_set,
        rawdata_dict,
        hostdns_init
    )

    # main database operation
    # initialize variables of function try_update()
    filter_dict = {'SerialNumber': SerialNumber}

    # call function try_update()
    try_update(
        SerialNumber,
        eval('Grains_HostDns'),
        eval('Grains_HostChgHistory'),
        hostdns,
        filter_dict
    )

# Grains_HostNICs
for hostname in vmhosts.iterkeys():
    # get special field's value
    SerialNumber = vmhosts[hostname]['serialnumber'].strip()

    nic_rawdata = vmhosts[hostname]['hwaddr_interfaces']
    ipv4_rawdata = vmhosts[hostname]['ip4_interfaces']
    ipv6_rawdata = vmhosts[hostname]['ip6_interfaces']
    TCP_port = unicode(vmhosts[hostname]['port']['TCP'])
    UDP_port = unicode(vmhosts[hostname]['port']['UDP'])

    for key, value in nic_rawdata.iteritems():
        hwaddr_interfaces = nic_rawdata[key]
        ip4_interfaces = unicode(ipv4_rawdata[key])
        try:
            ip6_interfaces = ipv6_rawdata[key][0]
        except IndexError, e:
            ip6_interfaces = ''

        # initialize fields dict
        hostnics = {
            'SerialNumber_id': SerialNumber,
            'nic_name': key,
            'hwaddr_interfaces': hwaddr_interfaces,
            'ip4_interfaces': ip4_interfaces,
            'ip6_interfaces': ip6_interfaces,
            'TCP_port': TCP_port,
            'UDP_port': UDP_port,
        }

        offlog_fields_set = {'TCP_port', 'UDP_port'}

        # main database operation
        # initialize variables of function try_update()
        filter_dict = {'hwaddr_interfaces': hostnics['hwaddr_interfaces']}

        # call function try_update()
        try_update(
            SerialNumber,
            eval('Grains_HostNICs'),
            eval('Grains_HostChgHistory'),
            hostnics,
            filter_dict,
            offlog_fields_set,
        )

# Grains_HostSaltInfo
for hostname in vmhosts.iterkeys():
    # get special field's value
    SerialNumber = vmhosts[hostname]['serialnumber'].strip()
    pythonpath = unicode(vmhosts[hostname]['pythonpath'])
    saltversioninfo = unicode(vmhosts[hostname]['saltversioninfo'])

    # initialize fields dict
    hostsaltinfo_init = {
        'SerialNumber_id': SerialNumber,
        'pythonpath': pythonpath,
        'saltversioninfo': saltversioninfo,
    }

    # initialize variables of function get_fields_dict()
    exclude_fields_set = {
        'SerialNumber',
        'pythonpath',
        'saltversioninfo',
    }

    rawdata_dict = vmhosts[hostname]

    # call function get_fields_dict()
    hostsaltinfo = get_fields_dict(
        'Grains_HostSaltInfo',
        exclude_fields_set,
        rawdata_dict,
        hostsaltinfo_init
    )

    # main database operation
    # initialize variables of function try_update()
    filter_dict = {'SerialNumber': SerialNumber}

    # call function try_update()
    try_update(
        SerialNumber,
        eval('Grains_HostSaltInfo'),
        eval('Grains_HostChgHistory'),
        hostsaltinfo,
        filter_dict
    )

# Grains_GuestGeneral
for hostname in vmguests.iterkeys():
    # get special field's value
    SerialNumber = vmguests[hostname]['serialnumber'].strip()
    defaultencoding = vmguests[hostname]['locale_info']['defaultencoding']
    defaultlanguage = vmguests[hostname]['locale_info']['defaultlanguage']
    detectedencoding = vmguests[hostname]['locale_info']['detectedencoding']
    osrelease_info = unicode(vmguests[hostname]['osrelease_info'])
    path = vmguests[hostname]['path'][:500]

    try:
        selinux = unicode(vmguests[hostname]['selinux'])
    except KeyError:
        selinux = ''

    try:
        osmajorrelease = unicode(vmguests[hostname]['osmajorrelease'])
    except KeyError:
        osmajorrelease = ''

    # initialize fields dict
    guest_general_init = {
        'SerialNumber_id': SerialNumber,
        'defaultencoding': defaultencoding,
        'defaultlanguage': defaultlanguage,
        'detectedencoding': detectedencoding,
        'osrelease_info': osrelease_info,
        'selinux': selinux,
        'osmajorrelease': osmajorrelease,
        'path': path,
    }

    # initialize variables of function get_fields_dict()
    exclude_fields_set = {
        'SerialNumber',
        'defaultencoding',
        'defaultlanguage',
        'detectedencoding',
        'osrelease_info',
        'selinux',
        'osmajorrelease',
        'path',
    }

    rawdata_dict = vmguests[hostname]

    # call function get_fields_dict()
    guest_general = get_fields_dict(
        'Grains_GuestGeneral',
        exclude_fields_set,
        rawdata_dict,
        guest_general_init
    )

    # main database operation
    # initialize variables of function try_update()
    filter_dict = {'SerialNumber': SerialNumber}

    # call function try_update()
    try:
        try_update(
            SerialNumber,
            eval('Grains_GuestGeneral'),
            eval('Grains_GuestChgHistory'),
            guest_general,
            filter_dict
        )
    except IndexError, e:
        errmsg = repr(e)
        tracebackmsg = traceback.format_exc()
        capture_date = timezone.now()

        exception = {
            'localhost': hostname,
            'SerialNumber': SerialNumber,
            'errmsg': errmsg,
            'tracebackmsg': tracebackmsg,
            'capture_date': capture_date,
        }

        Grains_Exception.objects.create(**exception)


# Grains_GuestHw
for hostname in vmguests.iterkeys():
    # get special field's value
    SerialNumber = vmguests[hostname]['serialnumber'].strip()
    mem_total = int(round(vmguests[hostname]['mem_total'] / 1024.0))

    if vmguests[hostname]['os'] == 'CentOS':
        cpu_flags = unicode(vmguests[hostname]['cpu_flags'])
        disks = unicode(vmguests[hostname]['disks'])
        SSDs = unicode(vmguests[hostname]['SSDs'])
        mdadm = unicode(vmguests[hostname]['mdadm'])
    else:
        cpu_flags = ''
        disks = ''
        SSDs = ''
        mdadm = ''

    try:
        ldisk_rawdata = vmguests[hostname]['ldisk']
        ldisk_size = {}
        for disk in ldisk_rawdata.iterkeys():
            if ldisk_rawdata[disk]['Size'].isdigit():
                size = int(
                    round(int(ldisk_rawdata[disk]['Size']) / 1024 / 1024 / 1024.0))
            else:
                size = ''
            ldisk_size.update({disk: size})
        ldisk_free = {}
        for disk in ldisk_rawdata.iterkeys():
            if ldisk_rawdata[disk]['FreeSpace'].isdigit():
                free = int(
                    round(int(ldisk_rawdata[disk]['FreeSpace']) / 1024 / 1024 / 1024.0))
            else:
                free = ''
            ldisk_free.update({disk: free})

        ldisk_size = unicode(ldisk_size)
        ldisk_free = unicode(ldisk_free)
    except KeyError:
        ldisk_size = ''
        ldisk_free = ''

    # initialize fields dict
    guesthw_init = {
        'SerialNumber_id': SerialNumber,
        'mem_total': mem_total,
        'cpu_flags': cpu_flags,
        'disks': disks,
        'SSDs': SSDs,
        'mdadm': mdadm,
        'ldisk_size': ldisk_size,
        'ldisk_free': ldisk_free,
    }

    # initialize variables of function get_fields_dict()
    exclude_fields_set = {
        'SerialNumber',
        'mem_total',
        'cpu_flags',
        'disks',
        'SSDs',
        'mdadm',
        'ldisk_size',
        'ldisk_free',
    }

    rawdata_dict = vmguests[hostname]

    # call function get_fields_dict()
    guesthw = get_fields_dict(
        'Grains_GuestHw',
        exclude_fields_set,
        rawdata_dict,
        guesthw_init
    )

    offlog_fields_set = {'ldisk_free'}

    # main database operation
    # initialize variables of function try_update()
    filter_dict = {'SerialNumber': SerialNumber}

    # call function try_update()
    try:
        try_update(
            SerialNumber,
            eval('Grains_GuestHw'),
            eval('Grains_GuestChgHistory'),
            guesthw,
            filter_dict,
            offlog_fields_set,
        )
    except IndexError, e:
        errmsg = repr(e)
        tracebackmsg = traceback.format_exc()
        capture_date = timezone.now()

        exception = {
            'localhost': hostname,
            'SerialNumber': SerialNumber,
            'errmsg': errmsg,
            'tracebackmsg': tracebackmsg,
            'capture_date': capture_date,
        }

        Grains_Exception.objects.create(**exception)

# Grains_GuestDns
for hostname in vmguests.iterkeys():
    # get special field's value
    SerialNumber = vmguests[hostname]['serialnumber'].strip()
    if vmguests[hostname]['os'] == 'Windows':
        nameservers = unicode(vmguests[hostname]['nameservers'])
        options = ''
        search = ''
        sortlist = ''
    else:
        nameservers = unicode(vmguests[hostname]['dns']['nameservers'])
        options = unicode(vmguests[hostname]['dns']['options'])
        search = unicode(vmguests[hostname]['dns']['search'])
        sortlist = unicode(vmguests[hostname]['dns']['sortlist'])

    # initialize fields dict
    guestdns_init = {
        'SerialNumber_id': SerialNumber,
        'nameservers': nameservers,
        'options': options,
        'search': search,
        'sortlist': sortlist,
    }

    # initialize variables of function get_fields_dict()
    exclude_fields_set = {
        'SerialNumber',
        'nameservers',
        'options',
        'search',
        'sortlist',
    }

    rawdata_dict = vmguests[hostname]

    # call function get_fields_dict()
    guestdns = get_fields_dict(
        'Grains_GuestDns',
        exclude_fields_set,
        rawdata_dict,
        guestdns_init
    )

    # main database operation
    # initialize variables of function try_update()
    filter_dict = {'SerialNumber': SerialNumber}

    # call function try_update()
    try:
        try_update(
            SerialNumber,
            eval('Grains_GuestDns'),
            eval('Grains_GuestChgHistory'),
            guestdns,
            filter_dict
        )
    except IndexError, e:
        errmsg = repr(e)
        tracebackmsg = traceback.format_exc()
        capture_date = timezone.now()

        exception = {
            'localhost': hostname,
            'SerialNumber': SerialNumber,
            'errmsg': errmsg,
            'tracebackmsg': tracebackmsg,
            'capture_date': capture_date,
        }

        Grains_Exception.objects.create(**exception)

# Grains_GuestNICs
for hostname in vmguests.iterkeys():
    # get special field's value
    SerialNumber = vmguests[hostname]['serialnumber'].strip()

    nic_rawdata = vmguests[hostname]['hwaddr_interfaces']
    ipv4_rawdata = vmguests[hostname]['ip4_interfaces']
    ipv6_rawdata = vmguests[hostname]['ip6_interfaces']
    tcp_port = unicode(vmguests[hostname]['port']['TCP'])
    udp_port = unicode(vmguests[hostname]['port']['UDP'])

    for key, value in nic_rawdata.iteritems():
        hwaddr_interfaces = nic_rawdata[key]
        ip4_interfaces = unicode(ipv4_rawdata[key])
        try:
            ip6_interfaces = ipv6_rawdata[key][0]
        except IndexError, e:
            ip6_interfaces = ''

        # initialize fields dict
        guestnics = {
            'SerialNumber_id': SerialNumber,
            'nic_name': key,
            'hwaddr_interfaces': hwaddr_interfaces,
            'ip4_interfaces': ip4_interfaces,
            'ip6_interfaces': ip6_interfaces,
            'TCP_port': tcp_port,
            'UDP_port': udp_port,
        }

        offlog_fields_set = {'TCP_port', 'UDP_port'}

        # main database operation
        # initialize variables of function try_update()
        filter_dict = {'SerialNumber': guestnics['SerialNumber_id'],
                       'hwaddr_interfaces': guestnics['hwaddr_interfaces']}

        # call function try_update()
        try:
            try_update(
                SerialNumber,
                eval('Grains_GuestNICs'),
                eval('Grains_GuestChgHistory'),
                guestnics,
                filter_dict,
                offlog_fields_set,
            )
        except (IndexError, django.db.utils.IntegrityError), e:
            errmsg = repr(e)
            tracebackmsg = traceback.format_exc()
            capture_date = timezone.now()

            exception = {
                'localhost': hostname,
                'SerialNumber': SerialNumber,
                'errmsg': errmsg,
                'tracebackmsg': tracebackmsg,
                'capture_date': capture_date,
            }

            Grains_Exception.objects.create(**exception)

# Grains_GuestSaltInfo
for hostname in vmguests.iterkeys():
    # get special field's value
    SerialNumber = vmguests[hostname]['serialnumber'].strip()
    pythonpath = unicode(vmguests[hostname]['pythonpath'])
    saltversioninfo = unicode(vmguests[hostname]['saltversioninfo'])

    # initialize fields dict
    guestsaltinfo_init = {
        'SerialNumber_id': SerialNumber,
        'pythonpath': pythonpath,
        'saltversioninfo': saltversioninfo,
    }

    # initialize variables of function get_fields_dict()
    exclude_fields_set = {
        'SerialNumber',
        'pythonpath',
        'saltversioninfo',
    }

    rawdata_dict = vmguests[hostname]

    # call function get_fields_dict()
    guestsaltinfo = get_fields_dict(
        'Grains_GuestSaltInfo',
        exclude_fields_set,
        rawdata_dict,
        guestsaltinfo_init
    )

    # main database operation
    # initialize variables of function try_update()
    filter_dict = {'SerialNumber': SerialNumber}

    # call function try_update()
    try:
        try_update(
            SerialNumber,
            eval('Grains_GuestSaltInfo'),
            eval('Grains_GuestChgHistory'),
            guestsaltinfo,
            filter_dict
        )
    except IndexError, e:
        errmsg = repr(e)
        tracebackmsg = traceback.format_exc()
        capture_date = timezone.now()

        exception = {
            'localhost': hostname,
            'SerialNumber': SerialNumber,
            'errmsg': errmsg,
            'tracebackmsg': tracebackmsg,
            'capture_date': capture_date,
        }

        Grains_Exception.objects.create(**exception)
