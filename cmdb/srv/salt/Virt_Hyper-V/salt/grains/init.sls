get_vmguest.ps1:
  file.managed:
    - name: c:\srv\salt\Virt_Hyper-V\salt\grains\files\get_vmguest.ps1
    - source: salt://Virt_Hyper-V/salt/grains/files/get_vmguest.ps1
    - makedirs: True

get_vmhost.ps1:
  file.managed:
    - name: c:\srv\salt\Virt_Hyper-V\salt\grains\files\get_vmhost.ps1
    - source: salt://Virt_Hyper-V/salt/grains/files/get_vmhost.ps1
    - makedirs: True

get_vmsn.ps1:
  file.managed:
    - name: c:\srv\salt\Virt_Hyper-V\salt\grains\files\get_vmsn.ps1
    - source: salt://Virt_Hyper-V/salt/grains/files/get_vmsn.ps1
    - makedirs: True
