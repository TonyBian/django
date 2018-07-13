#!/bin/bash

source ~/.bash_profile

DIRNAME=$(cd `dirname $0`; pwd)
BASE_DIRNAME=$(cd `dirname $DIRNAME`; pwd)
DJANGO_HOME=$BASE_DIRNAME/django
LOG_DIR=$BASE_DIRNAME/logs/cmdb

DATE=`date +%Y%m%d%H%M`

mkdir -p $LOG_DIR

PROC="ps -ef | grep "$0" | grep -v grep | grep -v vim"
PROC_COUNT=`ps -ef | grep "$0" | grep -v grep | grep -v vim | wc -l`

if [ "$PROC_COUNT" -gt 3 ]; then
    echo "$0 is already running."
    echo `ps -ef | grep "$0" | grep -v grep | grep -v vim`
    exit 1
fi

sh $BASE_DIRNAME/scripts/state_update.sh > $LOG_DIR/cmdb_main.$DATE.log 2>&1
`which python` $DJANGO_HOME/scripts/cmdb_update.py >> $LOG_DIR/cmdb_main.$DATE.log 2>&1
