#!/usr/bin/env python
# coding: utf-8

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2017-09-18 17:39

""""""

from django.conf.urls import url
from . import views

urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^(?P<provider>.+)/(?P<raw_view_name>.+)/$', views.index, name='index'),
    # url(r'^oracle/(.+)/$', views.oracle_db, name='oracle_db'),
    # url(r'^mysql/(.+)/$', views.mysql_db, name='mysql_db'),
    # url(r'^mssql/(.+)/$', views.mssql_db, name='mysql_db')
]
