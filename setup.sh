#!/bin/bash
PROG_NAME=$0

print_help ()
{
    echo "Usage : $PROG_NAME <install|run>"
    exit 1
}

install_client ()
{
    echo "install client"
    rsync -avzp --delete qy@10.157.11.32:/home/qy/dev/xs-agent ./
    pip install -r ./xs-agent/src/client-requirements.txt
}

run_client ()
{
    cat ./xs-agent/server.env
    source ./xs-agent/server.env
    export PYTHONPATH="$(pwd)/xs-agent/src"
    exec python -m xsagent.client.run
}

if [ $# -ne 1 ]
then
    print_help
fi


case "$1" in
    install)
        install_client
        ;;
    run)
        run_client
        ;;
    *)
        print_help
        ;;
esac
