FROM python:2

MAINTAINER Ouahib El Hanchi <ouahib.el.hanchi@gmail.com>

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY scrapyd.conf /etc/scrapyd/scrapyd.conf

EXPOSE 6800

ENTRYPOINT ["scrapyd", "--pidfile="]
