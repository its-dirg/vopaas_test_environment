#!/bin/sh

FILE_LIST="`docker ps -q`"

if [ ! -z "$FILE_LIST" ]
then
    echo output ${FILE_LIST}
    docker kill $(docker ps -q)
    echo "Docker tried to stop all containers"
else
    echo "Did not try to kill any docker containers"
fi
