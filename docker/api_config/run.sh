#! /bin/bash

# Run docker motorizen_api
docker/api_config/stop.sh
docker container run -d --rm \
--name=motorizen_api \
-p 8000:8000 \
--network=postgres_network \
--network=redis_network \
--network=keycloak_network \
--network-alias=motorizen_api \
--hostname=motorizen_api \
--env-file=docker/api_config/api.env \
motorizen:api