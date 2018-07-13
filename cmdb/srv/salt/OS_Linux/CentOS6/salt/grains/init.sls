get_opstools.py:
  file.managed:
    - name: /srv/salt/OS_Linux/salt/grains/files/get_opstools.py
    - source: salt://OS_Linux/CentOS6/salt/grains/files/get_opstools.py
    - makedirs: True
get_port.py:
  file.managed:
    - name: /srv/salt/OS_Linux/salt/grains/files/get_port.py
    - source: salt://OS_Linux/CentOS6/salt/grains/files/get_port.py
    - makedirs: True
get_timezone.sh:
  file.managed:
    - name: /srv/salt/OS_Linux/salt/grains/files/get_timezone.sh
    - source: salt://OS_Linux/CentOS6/salt/grains/files/get_timezone.sh
    - makedirs: True
