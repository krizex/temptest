#!/bin/bash
HOST=0.0.0.0
PORT=8000

PROG_NAME=$0

print_help ()
{
    echo "Usage : $PROG_NAME <start|stop|debug>"
    exit 1
}

start ()
{
    echo "starting server"
    exec python3 -m xsagent.server.run
}

stop ()
{
    echo "killing server"
}

start_debug_server ()
{
    echo "starting debug"
}

if [ $# -ne 1 ]
then
    print_help
fi


case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    debug)
        start_debug_server
        ;;
    restart)
        stop
        start
        ;;
    *)
        print_help
       ;;
esac
