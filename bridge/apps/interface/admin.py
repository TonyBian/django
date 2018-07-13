from django.contrib import admin

# Register your models here.
from .models import ProviderInfo
from .models import CustomerInfo
from .models import IFInfo
from .models import LegalRequest
from .models import IllegalRequest


class IFInfoInline(admin.TabularInline):
    model = IFInfo
    fk_name = 'provider'
    extra = 0


class IFInfoInlineForCustomer(admin.TabularInline):
    model = IFInfo
    fk_name = 'customer'
    extra = 0


class LegalRequestInline(admin.TabularInline):
    model = LegalRequest
    extra = 0


class IllegalRequestInline(admin.TabularInline):
    model = IllegalRequest
    extra = 0


class ProviderInfoAdmin(admin.ModelAdmin):
    list_display = (
        'provider',
        'db_type',
        'db_host',
        'db_port',
        'sid_or_dbname',
        'db_user',
        'db_charset',
        'login_timeout',
        'query_timeout',
    )

    list_filter = ['db_type']
    search_fields = [
        'provider',
        'db_type',
        'db_host',
        'db_port',
        'sid_or_dbname',
        'db_user',
        'db_charset',
        'login_timeout',
        'query_timeout',
    ]

    inlines = [IFInfoInline, LegalRequestInline, IllegalRequestInline]


class CustomerInfoAdmin(admin.ModelAdmin):
    list_display = [
        'customer',
        'customer_ip_list',
        'description',
        'create_time',
    ]

    search_filds = [
        'customer',
        'customer_ip_list',
    ]

    inlines = [IFInfoInlineForCustomer]


class IFInfoAdmin(admin.ModelAdmin):
    list_display = (
        'provider',
        'view_name',
        'customer',
        'description',
        'create_time',
    )

    search_fields = [
        'provider',
        'view_name',
        'customer',
        'description',
    ]

    list_filter = ['provider', 'customer']


class LegalRequestAdmin(admin.ModelAdmin):
    list_display = (
        'ip_addr',
        'request_provider',
        'request_view',
        'create_time',
    )

    search_fields = [
        'ip_addr',
        'request_provider',
        'request_view',
    ]

    list_filter = ['ip_addr', 'request_provider', 'request_view']


class IllegalRequestAdmin(admin.ModelAdmin):
    list_display = (
        'ip_addr',
        'ip_white_list',
        'request_provider',
        'request_view',
        'reason',
        'create_time',
    )

    search_fields = [
        'ip_addr',
        'ip_white_list',
        'request_provider',
        'request_view',
    ]

    list_filter = ['ip_addr', 'ip_white_list', 'request_provider', 'reason']


admin.site.register(ProviderInfo, ProviderInfoAdmin)
admin.site.register(CustomerInfo, CustomerInfoAdmin)
admin.site.register(IFInfo, IFInfoAdmin)
admin.site.register(LegalRequest, LegalRequestAdmin)
admin.site.register(IllegalRequest, IllegalRequestAdmin)
