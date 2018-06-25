FROM python:2

MAINTAINER Ouahib El Hanchi <ouahib.el.hanchi@gmail.com>

WORKDIR /usr/src/pipeline

COPY . .

RUN make install

CMD ["make", "deploy"]
