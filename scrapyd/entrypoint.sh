#!/bin/sh

envtpl /etc/scrapyd/scrapyd.conf.tpl --keep-template

scrapyd --pidfile=
