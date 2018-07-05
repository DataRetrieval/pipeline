FROM ruby:alpine

MAINTAINER Ouahib El Hanchi <ouahib.el.hanchi@gmail.com>

RUN apk add --no-cache tor haproxy privoxy

RUN gem install --no-ri --no-rdoc socksify

COPY haproxy.cfg.erb /usr/local/etc/haproxy.cfg.erb
COPY privoxy.cfg.erb /usr/local/etc/privoxy.cfg.erb
COPY torrc.erb /usr/local/etc/torrc.erb

COPY start.rb /usr/local/bin/start.rb
RUN chmod +x /usr/local/bin/start.rb

EXPOSE ${PRIVOXY_PORT:-8118}
EXPOSE ${HAPROXY_PORT:-5566}
EXPOSE ${HAPROXY_MONITOR_PORT:-2090}

ENTRYPOINT ["start.rb"]
