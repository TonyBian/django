base:
  '*':
    {% if grains['os'] == 'Windows' and grains['productname'] != 'Virtual Machine' %}
    - Virt_Hyper-V
    {% endif %}
    
    {% if grains['os'] == 'Windows' %}
    - OS_Windows
    {% endif %}

    {% if grains['os'] == 'CentOS' and grains['osmajorrelease'] == 6 %}
    - OS_Linux.CentOS6
    {% endif %}

    {% if grains['ipv4'][0].split('.')[2] == '211' or grains['nodename'].split('.')[0].upper() in ('BJ-TEST', 'BJ-TEST02', 'BJTEST02', 'BJTEST03', 'BJVMS05') %}
    - dev
    {% endif %}
