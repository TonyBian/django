from django.db import models

# Create your models here.
from django.utils import timezone


class ProviderInfo(models.Model):
    DB_TYPE_CHOICES = (
        ('mysql', 'MySQL 5.7'),
        ('oracle', 'Oracle 11.2.0.4'),
        ('mssql', 'SQLServer 2012'),
    )
    DB_CHARSET_CHOICES = (
        ('utf8', 'MySQL: utf8'),
        ('utf8mb4', 'MySQL: utf8mb4'),
        ('SIMPLIFIED CHINESE_CHINA.ZHS16GBK',
         'Oracle: SIMPLIFIED CHINESE_CHINA.ZHS16GBK'),
        ('SIMPLIFIED CHINESE_CHINA.UTF8', 'Oracle: SIMPLIFIED CHINESE_CHINA.UTF8'),
        ('AMERICAN_AMERICA.AL16UTF16', 'Oracle: AMERICAN_AMERICA.AL16UTF16'),
        ('cp936', 'SQLServer: cp936'),
    )
    provider = models.CharField(max_length=20, unique=True)
    db_type = models.CharField(max_length=20, choices=DB_TYPE_CHOICES)
    db_host = models.CharField(max_length=100)
    db_port = models.IntegerField()
    sid_or_dbname = models.CharField(max_length=20)
    db_user = models.CharField(max_length=20)
    db_passwd = models.CharField(max_length=50)
    db_charset = models.CharField(max_length=50, choices=DB_CHARSET_CHOICES)
    login_timeout = models.IntegerField(default=30)
    query_timeout = models.IntegerField(default=300)
    create_time = models.CharField(max_length=100, default=timezone.now())

    def __str__(self):
        return self.provider

    class Meta:
        verbose_name = "数据提供者配置"
        verbose_name_plural = verbose_name
        ordering = ['provider']


class CustomerInfo(models.Model):
    customer = models.CharField(max_length=20, unique=True)
    customer_ip_list = models.CharField(max_length=500)
    description = models.CharField(max_length=500, blank=True)
    create_time = models.CharField(max_length=100, default=timezone.now())

    def __str__(self):
        return self.customer

    class Meta:
        verbose_name = "数据消费者配置"
        verbose_name_plural = verbose_name
        ordering = ['customer']


class IFInfo(models.Model):
    provider = models.ForeignKey(
        ProviderInfo, to_field='provider')
    customer = models.ForeignKey(
        CustomerInfo, to_field='customer')
    view_name = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)
    create_time = models.CharField(max_length=100, default=timezone.now())

    def __str__(self):
        return self.provider_id

    class Meta:
        verbose_name = "接口配置"
        verbose_name_plural = verbose_name
        ordering = ['provider']


class IllegalRequest(models.Model):
    ip_addr = models.CharField(max_length=100)
    ip_white_list = models.CharField(max_length=500, blank=True)
    request_provider = models.ForeignKey(ProviderInfo, to_field='provider')
    request_view = models.CharField(max_length=100)
    reason = models.CharField(max_length=500, blank=True)
    create_time = models.CharField(max_length=100, default=timezone.now())

    def __str__(self):
        return self.request_provider_id

    class Meta:
        verbose_name = "非法访问记录"
        verbose_name_plural = verbose_name
        ordering = ['create_time']


class LegalRequest(models.Model):
    ip_addr = models.CharField(max_length=100)
    request_provider = models.ForeignKey(ProviderInfo, to_field='provider')
    request_view = models.CharField(max_length=100)
    create_time = models.CharField(max_length=100, default=timezone.now())

    def __str__(self):
        return self.request_provider_id

    class Meta:
        verbose_name = "合法访问记录"
        verbose_name_plural = verbose_name
        ordering = ['create_time']
