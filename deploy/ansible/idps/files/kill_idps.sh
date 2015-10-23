
#!/bin/sh

FILE_LIST="`pgrep -lf idp.py`"

if [ ! -z "$FILE_LIST" ]
then
    echo output ${FILE_LIST}
    kill $(pgrep -lf idp.py | awk '{ print $1 }')
    echo "Killed idps"
else
    echo "Did not try to kill any idps"
fi
