#! /bin/bash

# Run docker redisinsight
docker container stop redisinsight
docker container rm redisinsight
docker container run -d --rm \
--name redisinsight \
-p 5540:5540 \
--network=redis_network \
--hostname=redisinsight \
redis/redisinsight:latest \
-v redisinsight:/data