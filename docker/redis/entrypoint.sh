#!/bin/sh

: "${REDIS_USER:?REDIS_USER must be set}"
: "${REDIS_PASSWORD:?REDIS_PASSWORD must be set}"
: "${REDIS_PORT:?REDIS_PORT must be set}"

sed -e "s/{{REDIS_USER}}/${REDIS_USER}/g" \
    -e "s/{{REDIS_PASSWORD}}/${REDIS_PASSWORD}/g" \
    -e "s/{{REDIS_PORT}}/${REDIS_PORT}/g" \
    /usr/local/etc/redis/redis.conf > /tmp/redis.conf

exec redis-server /tmp/redis.conf