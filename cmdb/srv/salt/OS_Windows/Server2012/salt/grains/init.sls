get_ldisk.ps1:
  file.managed:
    - name: c:\srv\salt\OS_Windows\salt\grains\files\get_ldisk.ps1
    - source: salt://OS_Windows/Server2012/salt/grains/files/get_ldisk.ps1
    - makedirs: True

get_nameservers.ps1:
  file.managed:
    - name: c:\srv\salt\OS_Windows\salt\grains\files\get_nameservers.ps1
    - source: salt://OS_Windows/Server2012/salt/grains/files/get_nameservers.ps1
    - makedirs: True

get_opstools.py:
  file.managed:
    - name: c:\srv\salt\OS_Windows\salt\grains\files\get_opstools.py
    - source: salt://OS_Windows/Server2012/salt/grains/files/get_opstools.py
    - makedirs: True

get_port.py:
  file.managed:
    - name: c:\srv\salt\OS_Windows\salt\grains\files\get_port.py
    - source: salt://OS_Windows/Server2012/salt/grains/files/get_port.py
    - makedirs: True
