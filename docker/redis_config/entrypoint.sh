#!/bin/sh

# Check if environment variables are set
if [ -z "${REDIS_PASSWORD}" ]; then
  echo "Error: REDIS_PASSWORD environment variable is not set." >&2
  exit 1
fi

# Replace the placeholders in redis.conf
sed -i "s/\${REDIS_PASSWORD}/${REDIS_PASSWORD}/g" /etc/redis/redis.conf

# Start Redis with the configuration
exec redis-server /etc/redis/redis.conf