_master.conf:
  file.managed:
    - name: /etc/salt/minion.d/_master.conf
    - source: salt://public/salt/minion.d/_master.conf
    - makedirs: True
