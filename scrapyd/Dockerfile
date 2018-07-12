FROM python:2

MAINTAINER Ouahib El Hanchi <ouahib.el.hanchi@gmail.com>

ENV SCRAPYD_HOST ${SCRAPYD_HOST:-0.0.0.0}
ENV SCRAPYD_PORT ${SCRAPYD_PORT:-6800}
ENV SCRAPYD_MAX_PROC ${SCRAPYD_MAX_PROC:-0}
ENV SCRAPYD_MAX_PROC_PER_CPU ${SCRAPYD_MAX_PROC_PER_CPU:-4}
ENV SCRAPYD_POLL_INTERVAL ${SCRAPYD_POLL_INTERVAL:-5}
ENV SCRAPYD_KEEP_JOBS ${SCRAPYD_KEEP_JOBS:-5} 
ENV SCRAPYD_KEEP_FINISHED ${SCRAPYD_KEEP_FINISHED:-100}

RUN pip install --no-cache-dir scrapy scrapyd-client \
    scrapy-fake-useragent scrapyd boto demjson \
    python-dateutil envtpl

COPY scrapyd.conf.tpl /etc/scrapyd/

COPY entrypoint.sh /usr/local/bin/

EXPOSE ${SCRAPYD_PORT}

ENTRYPOINT ["entrypoint.sh"]
