from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
import os
import json
import cx_Oracle
import MySQLdb
import pymssql
from datetime import datetime
from .models import ProviderInfo
from .models import CustomerInfo
from .models import IFInfo
from .models import IllegalRequest
from .models import LegalRequest


def as_dict(cursor):
    cols = [d[0] for d in cursor.description]

    def createrow(*args):
        return dict(zip(cols, args))
    return createrow


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.__str__()
        return json.JSONEncoder.default(self, obj)


def index(request, provider, raw_view_name):
    # 防止sql注入
    view_name_list = [name for name in raw_view_name.split(' ') if name != '']
    view_count = len(view_name_list)
    view_name = view_name_list[0]

    dbinfo = ProviderInfo.objects.get(provider=provider)
    ifinfo = IFInfo.objects.filter(
        provider=provider, view_name__iexact=raw_view_name).values()

    # 获取customer_id
    customer_set = set()
    for interface in ifinfo:
        customer_id = interface['customer_id']
        customer_set.add(customer_id)

    # 获取customer ip
    ip_dicts = CustomerInfo.objects.filter(
        customer__in=customer_set).values('customer_ip_list')
    all_ip = []
    for ip_dict in ip_dicts:
        raw_ip_list = ip_dict['customer_ip_list'].split(',')
        ip_list = [ip for ip in map(str.strip, raw_ip_list) if ip != '']
        all_ip.extend(ip_list)
    ip_set = set(all_ip)

    db_host = dbinfo.db_host.strip()
    db_port = dbinfo.db_port
    sid_or_dbname = dbinfo.sid_or_dbname.strip()
    db_user = dbinfo.db_user.strip()
    db_passwd = dbinfo.db_passwd.strip()
    db_charset = dbinfo.db_charset.strip()
    login_timeout = dbinfo.login_timeout
    query_timeout = dbinfo.query_timeout

    # 获取访问ip
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip_addr = request.META['HTTP_X_FORWARDED_FOR'].strip()
    else:
        ip_addr = request.META['REMOTE_ADDR'].strip()

    # 访问合法性判断
    if not ifinfo:
        reason = '接口不存在'
    elif view_count != 1:
        reason = 'view_name是非法的'
    elif (ip_addr not in ip_set) and ('*' not in ip_set):
        reason = '访问者ip不在ip白名单内，ip白名单为{}'.format(ip_set)

    if 'reason' in locals().keys():
        illegal_request = {
            'ip_addr': ip_addr,
            'ip_white_list': ip_set,
            'request_provider_id': provider,
            'request_view': raw_view_name,
            'reason': reason,
        }
        IllegalRequest.objects.create(**illegal_request)

        return HttpResponse('Your request is illegal!')

    # 创建数据库连接，获取数据
    if dbinfo.db_type == 'mysql':
        conn = MySQLdb.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            passwd=db_passwd,
            db=sid_or_dbname,
            charset=db_charset,
            cursorclass=MySQLdb.cursors.DictCursor,
        )
        cursor = conn.cursor()
        cursor.execute("select * from {}".format(view_name))
        raw_data = cursor.fetchall()

    elif dbinfo.db_type == 'oracle':
        os.environ['NLS_LANG'] = db_charset
        conn = cx_Oracle.connect(
            db_user,
            db_passwd,
            '{0}:{1}/{2}'.format(db_host, db_port, sid_or_dbname),
        )
        cursor = conn.cursor()
        cursor.execute("select * from {}".format(view_name))
        cursor.rowfactory = as_dict(cursor)
        raw_data = cursor.fetchall()

    elif dbinfo.db_type == 'mssql':
        conn = pymssql.connect(
            host='{0}:{1}'.format(db_host, db_port),
            user=db_user,
            password=db_passwd,
            database=sid_or_dbname,
            login_timeout=login_timeout,
            timeout=query_timeout,
            charset=db_charset,
            as_dict=True,
        )
        cursor = conn.cursor()
        cursor.execute("select * from {}".format(view_name))
        raw_data = cursor.fetchall()

    cursor.close()
    conn.close()
    data = json.dumps(raw_data, cls=DateEncoder)
    legal_request = {
        'ip_addr': ip_addr,
        'request_provider_id': provider,
        'request_view': view_name
    }
    LegalRequest.objects.create(**legal_request)

    return HttpResponse(data)
