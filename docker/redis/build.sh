#! /bin/bash

# Build docker motorizen_redis
docker/redis_config/stop.sh
docker image rm motorizen:redis
docker build -t motorizen:redis -f docker/redis_config/redis.dockerfile .
