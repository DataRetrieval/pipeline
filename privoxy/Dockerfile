FROM python:2-alpine

MAINTAINER Ouahib El Hanchi <ouahib.el.hanchi@gmail.com>

ENV PRIVOXY_HOST ${PRIVOXY_HOST:-0.0.0.0}
ENV PRIVOXT_PORT ${PRIVOXY_PORT:-8118}
ENV PRIVOXY_FORWARD_SOCKS ${PRIVOXY_FORWARD_SOCKS}
ENV PRIVOXY_FORWARD_HTTP ${PRIVOXY_FORWARD_HTTP}

WORKDIR /etc/privoxy

COPY config.tpl .

COPY entrypoint.sh /usr/local/bin/

RUN apk add --no-cache privoxy \
    && pip install envtpl

EXPOSE ${PRIVOXY_PORT}

ENTRYPOINT ["entrypoint.sh"]
