#!/bin/sh

CONFIG_FILE=/etc/haproxy/haproxy.cfg
PID_FILE=/var/run/haproxy.pid
TIMEOUT=600

haproxy -f $CONFIG_FILE

while :;
do
    export HAPROXY_BACKENDS=$(fetch-proxies.py)
    envtpl /etc/haproxy/haproxy.cfg.tpl --keep-template
    haproxy -f $CONFIG_FILE -p $PID_FILE -D -sf $(cat $PID_FILE)
    sleep $TIMEOUT
done
