#!/bin/bash
# -*- coding: utf-8 -*-

# Author        : Tony Bian <biantonghe@gmail.com>
# Last modified : 2018-06-28 10:05
# Filename      : salt-master_install.sh

curl -L https://bootstrap.saltstack.com -o install_salt.sh
sh install_salt.sh -P -M -N -y -x python2.7 git v2017.7.2        #使用python2.7安装指定版本salt-master
# sh install_salt.sh -P -M -N       #仅安装最新版本的salt

# sed -i 's/#master:.*/master: salt.tutujia.com/g' /etc/salt/minion

mkdir -p /etc/salt/master.d
mkdir -p /srv/salt/_grains
mkdir -p /srv/salt/_modules
mkdir -p /srv/salt-master
mkdir -p /srv/pillar
mkdir -p /srv/salt/win/repo-ng
mkdir -p /srv/salt/win/repo
mkdir -p /srv/salt/win/repo/winrepo.p

# cp conf/srv_roots.conf /etc/salt/master.d/

sed -i 's/#auto_accept:.*/auto_accept: True/g' /etc/salt/master
service salt-master restart

iptables -D INPUT -p tcp -m tcp --dport 4505 -j ACCEPT
iptables -I INPUT -p tcp -m tcp --dport 4505 -j ACCEPT
iptables -D INPUT -p tcp -m tcp --dport 4506 -j ACCEPT
iptables -I INPUT -p tcp -m tcp --dport 4506 -j ACCEPT
/etc/rc.d/init.d/iptables save
service iptables restart

cat > /etc/logrotate.d/salt-master <<EOF
/var/log/salt/master {
daily
missingok
rotate 7
nocompress
#delaycompress
notifempty
dateext
}
EOF
