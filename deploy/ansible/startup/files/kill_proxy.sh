
#!/bin/sh

FILE_LIST="`pgrep -lf proxy_server.py`"

if [ ! -z "$FILE_LIST" ]
then
    echo output ${FILE_LIST}
    kill $(pgrep -lf proxy_server.py | awk '{ print $1 }')
    echo "Killed idps"
else
    echo "Did not try to kill any proxy"
fi
