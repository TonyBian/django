salt-minion_restart.bat:
  file.managed:
    - name: c:\srv\salt\OS_Windows\ScheduleJob\files\salt-minion_restart.bat
    - source: salt://OS_Windows/Server2012/ScheduleJob/files/salt-minion_restart.bat
    - makedirs: True

restart_salt-minion:
  cmd.run:
    - name: 'schtasks /create /F /tn restart_salt-minion /tr c:\srv\salt\OS_Windows\ScheduleJob\files\salt-minion_restart.bat /st 00:50 /sc DAILY /ru "NT Authority\System"'
    - order: last
