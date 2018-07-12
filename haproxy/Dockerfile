FROM python:2-alpine

MAINTAINER Ouahib El Hanchi <ouahib.el.hanchi@gmail.com>

ENV HAPROXY_HOST ${HAPROXY_HOST:-127.0.0.1}
ENV HAPROXY_PORT ${HAPROXY_PORT:-5566}
ENV HAPROXY_MONITOR_PORT ${HAPPROXY_MONITOR_PORT:-2090}
ENV HAPROXY_MONITOR_USERNAME ${HAPROXY_MONITOR_USERNAME:-admin}
ENV HAPROXY_MONITOR_PASSWORD ${HAPROXY_MONITOR_PASSWORD:-admin}
ENV HAPROXY_BALANCE_ALGORITHM ${HAPROXY_BALANCE_ALGORITHM:-roundrobin}

WORKDIR /etc/haproxy

RUN apk add --no-cache haproxy \
    && pip install requests bs4 fake-useragent envtpl

COPY haproxy.cfg.tpl .

COPY fetch-proxies.py /usr/local/bin/

COPY entrypoint.sh /usr/local/bin/

EXPOSE ${HAPROXY_PORT} ${HAPROXY_MONITOR_PORT}

ENTRYPOINT ["entrypoint.sh"]
