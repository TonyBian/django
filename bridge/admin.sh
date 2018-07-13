#!/bin/bash

DIRNAME=$(cd $(dirname $0); pwd)
DJANGO_HOME=$DIRNAME
SETTINGS_FILE=$(find $DJANGO_HOME -mindepth 2 -maxdepth 2 -name "settings.py")

if [ "$SETTINGS_FILE" == '' ]; then
    echo -e "\033[31mSettings.py file does not exist!\033[0m"
    exit 1
fi

APP_NAME=$2
PYTHON=$(command -v python)
PORT=$(grep "^PORT" $SETTINGS_FILE | awk -F "[ =]+" '{print $2}')
PROJECT_NAME=$(grep "^ROOT_URLCONF" $SETTINGS_FILE | awk -F "['.]" '{print $2}')
DEBUG=$(grep "^DEBUG" $SETTINGS_FILE | head -1 | awk -F "[ =]+" '{print $2}')

if [ $DEBUG == 'True' ]; then
    DEBUG=$(echo -e "\033[31m$DEBUG\033[0m")
else
    DEBUG=$(echo -e "\033[32m$DEBUG\033[0m")
fi

start()
{
    if netstat -tnpl | grep -- ":${PORT}\>" | grep -q python; then
        PID=$(netstat -tnpl | grep -- ":${PORT}\>" | awk -F "[ /]+" '{print $7}')
        echo -e "\033[31mPort ${PORT} is used by process \033[33m$PID\033[0m, \033[31mthe details are as follows:\033[0m"
        echo -e "\033[33mPID   PORT  COMMAND\033[0m"
        showall | grep -- ":${PORT}\>"
        exit 1
    fi
    nohup $PYTHON $DJANGO_HOME/manage.py runserver 0.0.0.0:$PORT > /dev/null 2>&1 &
}

stop()
{
    if netstat -tnpl | grep -- ":${PORT}\>" | grep -q python; then
        PID=$(netstat -tnpl | grep -- ":${PORT}\>" | awk -F "[ /]+" '{print $7}')
        kill -9 $PID
    fi
}

status()
{
    if netstat -tnpl | grep -- ":${PORT}\>" | grep -q python; then
        PID=$(netstat -tnpl | grep -- ":${PORT}\>" | awk -F "[ /]+" '{print $7}')
        RUNTIME_PYTHON=$(ps -ef | grep -- "$PID\>" | grep -v grep | awk '{print $8}')
        PYTHON_VERSION=$($RUNTIME_PYTHON -c "import platform; print(platform.python_version())")
        DJANGO_VERSION=$($RUNTIME_PYTHON -c "import django; print(django.get_version())")
        PYTHON_LIBRARY=$($RUNTIME_PYTHON -c "import sys; print(sys.path[-1])")
        APP_LIST=$(cd $DJANGO_HOME && $RUNTIME_PYTHON -c "from mysite import settings;print([appname for appname in settings.INSTALLED_APPS if appname[:6] != 'django'])")
        DATA_SOURCE_LIST=$(cd $DJANGO_HOME && $RUNTIME_PYTHON -c "from mysite import settings;print([db for db in settings.DATABASES.keys()])")
        PROC_INFO=$(ps -e -o 'pid,pcpu,pmem,rsz,vsz,etime,user' | awk 'gsub(/^ *| *$/,"")' | grep -- "^$PID\>")
        CPU=$(echo $PROC_INFO | awk '{print $2}')
        MEM=$(echo $PROC_INFO | awk '{print $3}')
        RES=$(echo $PROC_INFO | awk '{print $4}')
        VIRT=$(echo $PROC_INFO | awk '{print $5}')
        ETIME=$(echo $PROC_INFO | awk '{print $6}')
        USER=$(echo $PROC_INFO | awk '{print $7}')
        echo -e "\033[32mDjango project (pid $PID) is running...\033[0m"
        echo "Runtime Information:"
        echo "    Start User:     $USER"
        echo "    Project Name:   $PROJECT_NAME"
        echo "    APP List:       $APP_LIST"
        echo "    DBS List:       $DATA_SOURCE_LIST"
        echo "    Debug Mode:     $DEBUG"
        echo "    Root Path:      $DIRNAME"
        echo "    Settings File:  $SETTINGS_FILE"
        echo "    Web Port:       $PORT"
        echo "    Python Version: $PYTHON_VERSION"
        echo "    Django Version: $DJANGO_VERSION"
        echo "    Python Library: $PYTHON_LIBRARY"
        echo "Performance Information:"
        echo "    Elapsed:        $ETIME"
        echo "    %CPU:           $CPU"
        echo "    %MEM:           $MEM"
        echo "    RES:            $(expr $RES / 1024)m"
        echo "    VIRT:           $(expr $VIRT / 1024)m"
    else
        echo -e "\033[31mDjango project (\033[33m$PROJECT_NAME\033[31m) is stopped.\033[0m"
    fi
}

showall()
{
    echo -e "\033[33mPID   PORT  COMMAND\033[0m"
    netstat -tnlp | grep python | while read line; do
        PID=$(echo $line | awk -F "[ /]+" '{print $7}')
        PORT=$(echo $line | awk -F "[: ]+" '{print $5}')
        COMMAND=$(ps -ef | grep -- " $PID\>" | grep -v grep | grep "manage.py runserver" |  awk '{for(i=8;i<12;i++)printf $i" "}')
        if [ "$COMMAND" != '' ]; then
            printf "%-5s %-5s %s\n" $PID $PORT "$COMMAND"
        fi
    done
}

migrate()
{
DATABASES=`$PYTHON $DJANGO_HOME/manage.py shell <<EOF
from django.conf import settings
for db in settings.DATABASES.keys():
    print(db, end=' ')
EOF`

    if [ "$APP_NAME" = '' ]; then
        for i in $DATABASES; do
            $PYTHON $DJANGO_HOME/manage.py makemigrations
            $PYTHON $DJANGO_HOME/manage.py migrate --database=$i
        done
    else
        $PYTHON $DJANGO_HOME/manage.py makemigrations $APP_NAME
        $PYTHON $DJANGO_HOME/manage.py migrate $APP_NAME
    fi
}

debug()
{
    $PYTHON $DJANGO_HOME/manage.py runserver 0.0.0.0:$PORT
}

case "$1" in
    start)
        start
        sleep 2s
        status
        ;;
    stop)
        stop
        sleep 2s
        status
        ;;
    restart)
        stop
        sleep 2s
        start
        sleep 2s
        status
        ;;
    status)
        status
        ;;
    showall)
        showall
        ;;
    migrate)
        migrate
        ;;
    debug)
        stop
        sleep 2s
        debug
        ;;
    *)
        start=`echo -e "\033[34mstart\033[0m"`
        stop=`echo -e "\033[34mstop\033[0m"`
        restart=`echo -e "\033[34mrestart\033[0m"`
        status=`echo -e "\033[34mstatus\033[0m"`
        showall=`echo -e "\033[34mshowall\033[0m"`
        migrate=`echo -e "\033[34mmigrate\033[0m"`
        debug=`echo -e "\033[34mdebug\033[0m"`
	    echo "Usage: $0 {$start|$stop|$restart|$status|$showall|$migrate [<appname>]|$debug}"
        ;;
esac
