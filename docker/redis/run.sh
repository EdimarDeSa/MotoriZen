#! /bin/bash

# Run docker motorizen_redis
docker/redis_config/stop.sh
docker container run -d --rm \
--name=motorizen_redis \
-p 6379:6379 \
--network=redis_network \
--hostname=motorizen_redis \
--env-file=docker/redis_config/redis.env \
-v redis_data:/data \
motorizen:redis
