FROM python:3.6-alpine

RUN apk update \
    && apk add --no-cache --virtual bash \
    && apk add gcc \
    && apk add musl-dev \
    && apk add linux-headers \
    && apk add jpeg-dev \
    && apk add zlib-dev \
    && apk add postgresql-dev \
    && apk add libffi-dev

COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY uwsgi.ini /uwsgi.ini
CMD ["uwsgi", "--ini", "/uwsgi.ini"]