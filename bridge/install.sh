#!/bin/bash
# -*- coding: utf-8 -*-

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2018-02-08 21:59
# Filename      : install.sh

yum -y install mysql-devel

pip install mysqlclient
pip install cx_Oracle
pip install django-sqlserver
export PYMSSQL_BUILD_WITH_BUNDLED_FREETDS=1
pip install pymssql

rpm -ivh package/oracle-instantclient11.2-basic-11.2.0.4.0-1.x86_64.rpm
sh -c "echo /usr/lib/oracle/11.2/client64/lib > /etc/ld.so.conf.d/oracle-instantclient.conf"

ldconfig

cat >/etc/profile.d/oracle_client.sh <<EOF
export LD_LIBRARY_PATH=/usr/lib/oracle/11.2/client64/lib:\$LD_LIBRARY_PATH
EOF
