FROM python:2

MAINTAINER Ouahib El Hanchi <ouahib.el.hanchi@gmail.com>

ENV SCRAPYD_HOST ${SCRAPYD_HOST:-0.0.0.0}
ENV SCRAPYD_PORT ${SCRAPYD_PORT:-6800}
ENV SCRAPYD_MAX_PROC ${SCRAPYD_MAX_PROC:-0}
ENV SCRAPYD_MAX_PROC_PER_CPU ${SCRAPYD_MAX_PROC_PER_CPU:-4}
ENV SCRAPYD_POLL_INTERVAL ${SCRAPYD_POLL_INTERVAL:-5}
ENV SCRAPYD_KEEP_JOBS ${SCRAPYD_KEEP_JOBS:-5} 
ENV SCRAPYD_KEEP_FINISHED ${SCRAPYD_KEEP_FINISHED:-100}

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY scrapyd.conf.tpl /etc/scrapyd/scrapyd.conf.tpl

RUN envtpl < /etc/scrapyd/scrapyd.conf.tpl > /etc/scrapyd/scrapyd.conf

EXPOSE ${SCRAPYD_PORT}

ENTRYPOINT ["scrapyd", "--pidfile="]
