#!/bin/bash

# Run docker keycloak
docker/keycloak_config/stop.sh
docker container run -d \
--name=motorizen_keycloak \
-p 8080:8080 \
--network=keycloak_network \
--network-alias=motorizen_keycloak \
--hostname=motorizen_keycloak \
--env-file=docker/keycloak_config/keycloak.env \
--volume=keycloak_data:/opt/keycloak/data \
--volume=keycloak_conf:/opt/keycloak/conf \
motorizen:keycloak start-dev