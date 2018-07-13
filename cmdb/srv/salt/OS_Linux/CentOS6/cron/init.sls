/etc/init.d/salt-minion restart > /dev/null:
  cron.present:
    - user: root
    - minute: 50
    - hour: 0
    - daymonth: '*/1'
