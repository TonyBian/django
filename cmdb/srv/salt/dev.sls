_master_dev.conf:
  file.managed:
    - source: salt://public/salt/minion.d/_master_dev.conf
    {% if grains['os'] == 'Windows' %}
    - name: c:\\salt\\conf\\minion.d\\_master.conf
    {% elif grains['os'] == 'CentOS' %}
    - name: /etc/salt/minion.d/_master.conf
    {% endif %}
    - makedirs: True
