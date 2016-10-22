FROM gliderlabs/alpine:3.4

# base
RUN \
    apk update && apk upgrade \
    && apk add \
        python3 sudo bash htop ca-certificates openssl tini \
    && apk add build-base coreutils \
    && rm -f /var/cache/apk/*

ENTRYPOINT ["/sbin/tini", "--"]
CMD ["python3", "manage.py", "serve"]

COPY docker/dist /app
WORKDIR /app

# app
RUN apk update \
    && apk add --virtual build-dependencies python3-dev build-base \
    && pip3 install -r requirements.txt \
    && apk del --purge build-dependencies \
    && rm -f /var/cache/apk/* \
    && rm -rf /app/.cache


