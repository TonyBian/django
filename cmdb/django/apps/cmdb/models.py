# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

from django.utils import timezone


class Grains_Vmsn(models.Model):
    ElementName = models.CharField(max_length=255)
    BIOSSerialNumber = models.CharField(max_length=40, primary_key=True)
    VirtualSystemIdentifier = models.CharField(max_length=40, unique=True)
    osfullname = models.CharField(max_length=100, null=True)
    osrelease = models.CharField(max_length=20, null=True)
    hwaddr = models.CharField(max_length=255)
    ipv4 = models.CharField(max_length=255)
    titanagent = models.IntegerField(default=0)
    splunk = models.IntegerField(default=0)
    zabbix = models.IntegerField(default=0)
    IsExpired = models.IntegerField(default=0)
    ExpiredDate = models.CharField(max_length=80, null=True)

    def __unicode__(self):
        return self.BIOSSerialNumber

    def is_active(self):
        return not self.IsExpired

    is_active.admin_order_field = 'IsExpired'
    is_active.boolean = True
    is_active.short_description = 'Salt?'

    def is_titanagent_active(self):
        return self.titanagent

    is_titanagent_active.admin_order_field = 'titanagent'
    is_titanagent_active.boolean = True
    is_titanagent_active.short_description = 'titanagent?'

    def is_splunk_active(self):
        return self.splunk

    is_splunk_active.admin_order_field = 'splunk'
    is_splunk_active.boolean = True
    is_splunk_active.short_description = 'Splunk?'

    def is_zabbix_active(self):
        return self.zabbix

    is_zabbix_active.admin_order_field = 'zabbix'
    is_zabbix_active.boolean = True
    is_zabbix_active.short_description = 'Zabbix?'

    class Meta:
        verbose_name = u"虚拟机详细信息"
        verbose_name_plural = verbose_name
        ordering = ['ElementName']
    #     db_table = 'cmdb_grains_vmsn'
    #     unique_together = ('BIOSSerialNumber', 'VirtualSystemIdentifier')


class Grains_Vmhost(models.Model):
    SerialNumber = models.CharField(max_length=40, primary_key=True)
    ComputerName = models.CharField(max_length=20)
    osfullname = models.CharField(max_length=100, null=True)
    FullyQualifiedDomainName = models.CharField(max_length=20)
    VMMigrationEnabled = models.CharField(max_length=10)
    MemoryCapacity = models.IntegerField()
    hwaddr = models.CharField(max_length=255)
    ipv4 = models.CharField(max_length=255)
    admin = models.CharField(max_length=20)
    titanagent = models.IntegerField(default=0)
    splunk = models.IntegerField(default=0)
    zabbix = models.IntegerField(default=0)
    IsExpired = models.IntegerField(default=0)
    ExpiredDate = models.CharField(max_length=80, null=True)

    def __unicode__(self):
        return self.SerialNumber

    def domainname(self):
        return self.FullyQualifiedDomainName

    domainname.short_description = 'DomainName'

    def is_active(self):
        return not self.IsExpired

    is_active.admin_order_field = 'IsExpired'
    is_active.boolean = True
    is_active.short_description = 'Salt?'

    def is_titanagent_active(self):
        return self.titanagent

    is_titanagent_active.admin_order_field = 'titanagent'
    is_titanagent_active.boolean = True
    is_titanagent_active.short_description = 'titanagent?'

    def is_splunk_active(self):
        return self.splunk

    is_splunk_active.admin_order_field = 'splunk'
    is_splunk_active.boolean = True
    is_splunk_active.short_description = 'Splunk?'

    def is_zabbix_active(self):
        return self.zabbix

    is_zabbix_active.admin_order_field = 'zabbix'
    is_zabbix_active.boolean = True
    is_zabbix_active.short_description = 'Zabbix?'

    class Meta:
        verbose_name = u"宿主机详细信息"
        verbose_name_plural = verbose_name
        ordering = ['ComputerName']


class Grains_Vmguest(models.Model):
    VirtualSystemIdentifier = models.ForeignKey(
        Grains_Vmsn,
        to_field='VirtualSystemIdentifier')
    HostSerialNumber = models.ForeignKey(
        Grains_Vmhost,
        to_field='SerialNumber')
    VMName = models.CharField(max_length=20)
    ComputerName = models.CharField(max_length=20)
    Path = models.CharField(max_length=500)
    CreationTime = models.CharField(max_length=100, null=True)
    State = models.CharField(max_length=20)
    ReplicationMode = models.CharField(max_length=20)
    MemoryAssigned = models.IntegerField()
    MemoryStartup = models.IntegerField()
    Notes = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return self.VirtualSystemIdentifier_id

    def is_active(self):
        return not self.IsExpired

    is_active.admin_order_field = 'IsExpired'
    is_active.boolean = True
    is_active.short_description = 'Is active?'

    class Meta:
        verbose_name = u"虚拟机概要信息"
        verbose_name_plural = verbose_name
        ordering = ['ComputerName', 'VMName']
    #     db_table = 'cmdb_grains_vmguest'
    #     unique_together = ('VM', 'HostSerialNumber')


class Grains_HostChgHistory(models.Model):
    SerialNumber = models.ForeignKey(
        Grains_Vmhost,
        to_field='SerialNumber')
    model_name = models.CharField(max_length=50)
    field_name = models.CharField(max_length=100)
    old_value = models.CharField(max_length=1000, null=True)
    new_value = models.CharField(max_length=1000, null=True)
    change_date = models.CharField(
        max_length=100, default=unicode(timezone.now()))

    def __unicode__(self):
        return self.SerialNumber_id

    class Meta:
        verbose_name = u"宿主机历史变更记录"
        verbose_name_plural = verbose_name


class Grains_GuestChgHistory(models.Model):
    SerialNumber = models.ForeignKey(
        Grains_Vmsn,
        to_field='BIOSSerialNumber')
    model_name = models.CharField(max_length=50)
    field_name = models.CharField(max_length=100)
    old_value = models.CharField(max_length=1000, null=True)
    new_value = models.CharField(max_length=1000, null=True)
    change_date = models.CharField(
        max_length=100, default=unicode(timezone.now()))

    def __unicode__(self):
        return self.SerialNumber_id

    class Meta:
        verbose_name = u"虚拟机历史变更记录"
        verbose_name_plural = verbose_name


class Grains_HostGeneral(models.Model):
    SerialNumber = models.OneToOneField(
        Grains_Vmhost,
        to_field='SerialNumber',
        primary_key=True)
    server_id = models.IntegerField()
    uuid = models.CharField(max_length=40, null=True)
    virtual = models.CharField(max_length=20, null=True)
    host = models.CharField(max_length=20, null=True)
    localhost = models.CharField(max_length=40, null=True)
    init = models.CharField(max_length=20, null=True)
    kernel = models.CharField(max_length=20, null=True)
    kernelrelease = models.CharField(max_length=200, null=True)
    lsb_distrib_codename = models.CharField(max_length=20, null=True)
    lsb_distrib_id = models.CharField(max_length=20, null=True)
    lsb_distrib_release = models.CharField(max_length=10, null=True)
    os = models.CharField(max_length=20, null=True)
    os_family = models.CharField(max_length=20, null=True)
    osarch = models.CharField(max_length=20, null=True)
    oscodename = models.CharField(max_length=20, null=True)
    osfinger = models.CharField(max_length=50, null=True)
    osfullname = models.CharField(max_length=100, null=True)
    osmanufacturer = models.CharField(max_length=50, null=True)
    osmajorrelease = models.CharField(max_length=10, null=True)
    osrelease = models.CharField(max_length=20, null=True)
    osrelease_info = models.CharField(max_length=10, null=True)
    osservicepack = models.CharField(max_length=10, null=True)
    osversion = models.CharField(max_length=20, null=True)
    path = models.CharField(max_length=500, null=True)
    ps = models.CharField(max_length=20, null=True)
    shell = models.CharField(max_length=20, null=True)
    timezone = models.CharField(max_length=100, null=True)
    defaultencoding = models.CharField(max_length=10, null=True)
    defaultlanguage = models.CharField(max_length=10, null=True)
    detectedencoding = models.CharField(max_length=10, null=True)
    selinux = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return self.SerialNumber_id

    class Meta:
        verbose_name = u"宿主机综合信息"
        verbose_name_plural = verbose_name


class Grains_GuestGeneral(models.Model):
    SerialNumber = models.OneToOneField(
        Grains_Vmsn,
        to_field='BIOSSerialNumber',
        primary_key=True)
    server_id = models.IntegerField()
    uuid = models.CharField(max_length=40, null=True)
    virtual = models.CharField(max_length=20, null=True)
    host = models.CharField(max_length=20, null=True)
    localhost = models.CharField(max_length=40, null=True)
    init = models.CharField(max_length=20, null=True)
    kernel = models.CharField(max_length=20, null=True)
    kernelrelease = models.CharField(max_length=200, null=True)
    lsb_distrib_codename = models.CharField(max_length=20, null=True)
    lsb_distrib_id = models.CharField(max_length=20, null=True)
    lsb_distrib_release = models.CharField(max_length=10, null=True)
    os = models.CharField(max_length=20, null=True)
    os_family = models.CharField(max_length=20, null=True)
    osarch = models.CharField(max_length=20, null=True)
    oscodename = models.CharField(max_length=20, null=True)
    osfinger = models.CharField(max_length=50, null=True)
    osfullname = models.CharField(max_length=100, null=True)
    osmanufacturer = models.CharField(max_length=50, null=True)
    osmajorrelease = models.CharField(max_length=10, null=True)
    osrelease = models.CharField(max_length=20, null=True)
    osrelease_info = models.CharField(max_length=10, null=True)
    osservicepack = models.CharField(max_length=10, null=True)
    osversion = models.CharField(max_length=20, null=True)
    path = models.CharField(max_length=500, null=True)
    ps = models.CharField(max_length=20, null=True)
    shell = models.CharField(max_length=20, null=True)
    timezone = models.CharField(max_length=100, null=True)
    defaultencoding = models.CharField(max_length=10, null=True)
    defaultlanguage = models.CharField(max_length=10, null=True)
    detectedencoding = models.CharField(max_length=10, null=True)
    selinux = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return self.SerialNumber_id

    class Meta:
        verbose_name = u"虚拟机综合信息"
        verbose_name_plural = verbose_name


class Grains_HostDns(models.Model):
    SerialNumber = models.OneToOneField(
        Grains_Vmhost,
        to_field='SerialNumber',
        primary_key=True)
    fqdn = models.CharField(max_length=40)
    domain = models.CharField(max_length=20)
    windowsdomain = models.CharField(max_length=20)
    nameservers = models.CharField(max_length=500)
    options = models.CharField(max_length=100)
    search = models.CharField(max_length=50)
    sortlist = models.CharField(max_length=20)

    def __unicode__(self):
        return self.SerialNumber_id

    class Meta:
        verbose_name = u"宿主机NDS信息"
        verbose_name_plural = verbose_name


class Grains_GuestDns(models.Model):
    SerialNumber = models.OneToOneField(
        Grains_Vmsn,
        to_field='BIOSSerialNumber',
        primary_key=True)
    fqdn = models.CharField(max_length=40)
    domain = models.CharField(max_length=20)
    windowsdomain = models.CharField(max_length=20)
    nameservers = models.CharField(max_length=500)
    options = models.CharField(max_length=100)
    search = models.CharField(max_length=50)
    sortlist = models.CharField(max_length=20)

    def __unicode__(self):
        return self.SerialNumber_id

    class Meta:
        verbose_name = u"虚拟机DNS信息"
        verbose_name_plural = verbose_name


class Grains_HostHw(models.Model):
    SerialNumber = models.OneToOneField(
        Grains_Vmhost,
        to_field='SerialNumber',
        primary_key=True)
    machine_id = models.CharField(max_length=40)
    manufacturer = models.CharField(max_length=50)
    productname = models.CharField(max_length=30)
    biosversion = models.CharField(max_length=100)
    biosreleasedate = models.CharField(max_length=40)
    cpu_model = models.CharField(max_length=100)
    cpuarch = models.CharField(max_length=10)
    cpu_flags = models.CharField(max_length=1000)
    num_cpus = models.IntegerField()
    num_gpus = models.IntegerField()
    mem_total = models.IntegerField()
    disks = models.CharField(max_length=1000)
    ldisk_size = models.CharField(max_length=200)
    ldisk_free = models.CharField(max_length=200)
    SSDs = models.CharField(max_length=100)
    mdadm = models.CharField(max_length=100)

    def __unicode__(self):
        return self.SerialNumber_id

    class Meta:
        verbose_name = u"宿主机硬件信息"
        verbose_name_plural = verbose_name


class Grains_GuestHw(models.Model):
    SerialNumber = models.OneToOneField(
        Grains_Vmsn,
        to_field='BIOSSerialNumber',
        primary_key=True)
    machine_id = models.CharField(max_length=40)
    manufacturer = models.CharField(max_length=50)
    productname = models.CharField(max_length=30)
    biosversion = models.CharField(max_length=100)
    biosreleasedate = models.CharField(max_length=40)
    cpu_model = models.CharField(max_length=100)
    cpuarch = models.CharField(max_length=10)
    cpu_flags = models.CharField(max_length=1000)
    num_cpus = models.IntegerField()
    num_gpus = models.IntegerField()
    mem_total = models.IntegerField()
    disks = models.CharField(max_length=1000)
    ldisk_size = models.CharField(max_length=200)
    ldisk_free = models.CharField(max_length=200)
    SSDs = models.CharField(max_length=100)
    mdadm = models.CharField(max_length=100)

    def __unicode__(self):
        return self.SerialNumber_id

    class Meta:
        verbose_name = u"虚拟机硬件信息"
        verbose_name_plural = verbose_name


class Grains_HostNICs(models.Model):
    SerialNumber = models.ForeignKey(
        Grains_Vmhost,
        to_field='SerialNumber')
    nic_name = models.CharField(max_length=100)
    hwaddr_interfaces = models.CharField(max_length=17)
    ip4_interfaces = models.CharField(max_length=500)
    ip6_interfaces = models.CharField(max_length=500)
    TCP_port = models.CharField(max_length=5000, null=True)
    UDP_port = models.CharField(max_length=5000, null=True)

    def __unicode__(self):
        return self.SerialNumber_id

    class Meta:
        db_table = 'cmdb_grains_hostnics'
        unique_together = ('SerialNumber', 'hwaddr_interfaces')

    class Meta:
        verbose_name = u"宿主机网卡信息"
        verbose_name_plural = verbose_name


class Grains_GuestNICs(models.Model):
    SerialNumber = models.ForeignKey(
        Grains_Vmsn,
        to_field='BIOSSerialNumber')
    nic_name = models.CharField(max_length=100)
    hwaddr_interfaces = models.CharField(max_length=17)
    ip4_interfaces = models.CharField(max_length=500)
    ip6_interfaces = models.CharField(max_length=500)
    TCP_port = models.CharField(max_length=5000, null=True)
    UDP_port = models.CharField(max_length=5000, null=True)

    def __unicode__(self):
        return self.SerialNumber_id

    class Meta:
        verbose_name = u"虚拟机网卡信息"
        verbose_name_plural = verbose_name
        unique_together = ('SerialNumber', 'hwaddr_interfaces')


class Grains_HostSaltInfo(models.Model):
    SerialNumber = models.OneToOneField(
        Grains_Vmhost,
        to_field='SerialNumber',
        primary_key=True)
    master = models.CharField(max_length=40)
    minion_id = models.CharField(max_length=40)
    nodename = models.CharField(max_length=50)
    pythonexecutable = models.CharField(max_length=40)
    pythonpath = models.CharField(max_length=1000)
    saltpath = models.CharField(max_length=100)
    saltversion = models.CharField(max_length=20)
    saltversioninfo = models.CharField(max_length=20)
    zmqversion = models.CharField(max_length=10)

    def __unicode__(self):
        return self.SerialNumber_id

    class Meta:
        verbose_name = u"宿主机salt信息"
        verbose_name_plural = verbose_name


class Grains_GuestSaltInfo(models.Model):
    SerialNumber = models.OneToOneField(
        Grains_Vmsn,
        to_field='BIOSSerialNumber',
        primary_key=True)
    master = models.CharField(max_length=40)
    minion_id = models.CharField(max_length=40)
    nodename = models.CharField(max_length=50)
    pythonexecutable = models.CharField(max_length=40)
    pythonpath = models.CharField(max_length=1000)
    saltpath = models.CharField(max_length=100)
    saltversion = models.CharField(max_length=20)
    saltversioninfo = models.CharField(max_length=20)
    zmqversion = models.CharField(max_length=10)

    def __unicode__(self):
        return self.SerialNumber_id

    class Meta:
        verbose_name = u"虚拟机salt信息"
        verbose_name_plural = verbose_name


class Grains_Exception(models.Model):
    localhost = models.CharField(max_length=40, null=True)
    SerialNumber = models.CharField(max_length=40)
    errmsg = models.CharField(max_length=2000)
    tracebackmsg = models.CharField(max_length=10000)
    capture_date = models.DateTimeField()

    def __unicode__(self):
        return self.SerialNumber

    class Meta:
        verbose_name = u"异常信息"
        verbose_name_plural = verbose_name
