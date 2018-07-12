#!/bin/sh

envtpl config.tpl --keep-template

privoxy --no-daemon
