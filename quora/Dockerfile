# syntax = docker/dockerfile:experimental

FROM python:3.8-alpine

WORKDIR /app
# ENV PATH="/scripts:${PATH}"

# RUN apk del .tmp



COPY ./requirements.txt ./requirements.txt

RUN apk add --update --virtual .tmp gcc g++ libxslt-dev libc-dev linux-headers musl-dev python3-dev mariadb-dev mariadb-connector-c-dev mariadb-dev build-base

RUN --mount=type=cache,target=/root/.cache pip install -r requirements.txt

RUN pip install -U pip

COPY . .

# RUN (crontab -l 2>/dev/null; echo "30 14,20 * * * python /app/manage.py sync_products >> /app/shared_data/cron-log.txt 2>&1") | crontab -

COPY ./entrypoint.sh ./

ENTRYPOINT ["sh", "entrypoint.sh"] 