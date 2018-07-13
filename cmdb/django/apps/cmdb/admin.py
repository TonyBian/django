# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from models import Grains_Vmsn
from models import Grains_Vmhost
from models import Grains_Vmguest
from models import Grains_HostGeneral
from models import Grains_HostHw
from models import Grains_HostDns
from models import Grains_HostNICs
from models import Grains_HostSaltInfo
from models import Grains_HostChgHistory
from models import Grains_GuestGeneral
from models import Grains_GuestHw
from models import Grains_GuestDns
from models import Grains_GuestNICs
from models import Grains_GuestSaltInfo
from models import Grains_GuestChgHistory
from models import Grains_Exception


# Grains_Vmguest Inline
class Grains_VmguestInline(admin.TabularInline):
    model = Grains_Vmguest
    extra = 0


# Grains_Vmhost configuration
class Grains_HostNICsInline(admin.TabularInline):
    model = Grains_HostNICs
    extra = 0


class Grains_HostDnsInline(admin.StackedInline):
    model = Grains_HostDns
    extra = 0


class Grains_HostGeneralInline(admin.StackedInline):
    model = Grains_HostGeneral
    extra = 0


class Grains_HostHwInline(admin.StackedInline):
    model = Grains_HostHw
    extra = 0


class Grains_HostSaltInfoInline(admin.StackedInline):
    model = Grains_HostSaltInfo
    extra = 0


class Grains_HostChgHistoryInline(admin.TabularInline):
    model = Grains_HostChgHistory
    extra = 0


class Grains_VmhostAdmin(admin.ModelAdmin):
    list_display = (
        'ComputerName',
        'SerialNumber',
        'osfullname',
        'domainname',
        'MemoryCapacity',
        'hwaddr',
        'ipv4',
        'admin',
        'is_titanagent_active',
        'is_splunk_active',
        'is_zabbix_active',
        'is_active',
        'ExpiredDate'
    )
    list_filter = ['IsExpired', 'zabbix', 'osfullname', 'MemoryCapacity', 'admin']
    search_fields = ['ComputerName', 'SerialNumber', 'hwaddr', 'ipv4', 'admin']
    inlines = [
        Grains_VmguestInline,
        Grains_HostNICsInline,
        Grains_HostDnsInline,
        Grains_HostGeneralInline,
        Grains_HostHwInline,
        Grains_HostSaltInfoInline,
        Grains_HostChgHistoryInline,
    ]


# Grains_Vmguest configuration
class Grains_GuestNICsInline(admin.TabularInline):
    model = Grains_GuestNICs
    extra = 0


class Grains_GuestDnsInline(admin.StackedInline):
    model = Grains_GuestDns
    extra = 0


class Grains_GuestGeneralInline(admin.StackedInline):
    model = Grains_GuestGeneral
    extra = 0


class Grains_GuestHwInline(admin.StackedInline):
    model = Grains_GuestHw
    extra = 0


class Grains_GuestSaltInfoInline(admin.StackedInline):
    model = Grains_GuestSaltInfo
    extra = 0


class Grains_GuestChgHistoryInline(admin.TabularInline):
    model = Grains_GuestChgHistory
    extra = 0


class Grains_VmsnAdmin(admin.ModelAdmin):
    list_display = (
        'ElementName',
        'BIOSSerialNumber',
        'VirtualSystemIdentifier',
        'osfullname',
        'osrelease',
        'hwaddr',
        'ipv4',
        'is_titanagent_active',
        'is_splunk_active',
        'is_zabbix_active',
        'is_active',
        'ExpiredDate',
    )
    list_filter = ['IsExpired',
                   'zabbix',
                   'osfullname',
                   'osrelease'
                   ]
    search_fields = ['ElementName',
                     'BIOSSerialNumber',
                     'VirtualSystemIdentifier',
                     'hwaddr',
                     'ipv4'
                     ]
    inlines = [
        Grains_VmguestInline,
        Grains_GuestNICsInline,
        Grains_GuestDnsInline,
        Grains_GuestGeneralInline,
        Grains_GuestHwInline,
        Grains_GuestSaltInfoInline,
        Grains_GuestChgHistoryInline,
    ]


class Grains_VmguestAdmin(admin.ModelAdmin):
    list_display = (
        'VMName',
        'ComputerName',
        'Path',
        'CreationTime',
        'State',
        'ReplicationMode',
        'MemoryAssigned',
        'MemoryStartup',
        'Notes',
    )
    list_filter = ['ComputerName', 'State', 'ReplicationMode', 'MemoryStartup']
    search_fields = ['VMName']


# Grains_Exception configuration
class Grains_ExceptionAdmin(admin.ModelAdmin):
    list_display = (
        'localhost',
        'SerialNumber',
        'errmsg',
        'tracebackmsg',
        'capture_date'
    )
    list_filter = ['localhost', 'errmsg']
    search_fields = ['localhost']


admin.site.register(Grains_Vmsn, Grains_VmsnAdmin)
admin.site.register(Grains_Vmhost, Grains_VmhostAdmin)
admin.site.register(Grains_Vmguest, Grains_VmguestAdmin)
admin.site.register(Grains_Exception, Grains_ExceptionAdmin)
