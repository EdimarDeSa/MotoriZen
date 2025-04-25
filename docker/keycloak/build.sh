#!/bin/bash

# Build docker keycloak
docker/keycloak_config/stop.sh
docker image rm motorizen:keycloak
docker image build -t motorizen:keycloak -f docker/keycloak_config/keycloak.dockerfile .