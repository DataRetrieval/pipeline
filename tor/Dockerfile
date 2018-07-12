FROM ruby:alpine

MAINTAINER Ouahib El Hanchi <ouahib.el.hanchi@gmail.com>

RUN apk add --no-cache tor

RUN gem install --no-ri --no-rdoc socksify

COPY torrc.erb /etc/tor/

COPY entrypoint.rb /usr/local/bin/

ENTRYPOINT ["entrypoint.rb"]
