FROM python:2

MAINTAINER Ouahib El Hanchi <ouahib.el.hanchi@gmail.com>

RUN pip install spiderkeeper

ENV HOST ${HOST:-0.0.0.0}
ENV PORT ${PORT:-5000}
ENV USER ${USER:-admin}
ENV PASS ${PASS:-admin}
ENV SERVER ${SERVER:-http://localhost:6800}
ENV DATABASE_URL ${DATABASE_URL:-sqlite:////var/lib/spiderkeeper/data.db}

EXPOSE ${PORT}

ENTRYPOINT spiderkeeper \
    --host=$HOST \
    --port=$PORT \
    --username=$USER \
    --password=$PASS \
    --server=$SERVER \
    --database-url=$DATABASE_URL
