#!/bin/sh
sleep 10
while [ $(curl {{ pyff_discovery_url }}/role/idp.xml 2>&1 devnull | wc -l) = 0 ]
do
echo "waiting for pyff..."
sleep 5
done
