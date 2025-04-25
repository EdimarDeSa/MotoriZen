#! /bin/bash

# Build docker motorizen_api
docker/api_config/stop.sh
docker image rm motorizen:api
docker build -t motorizen:api -f docker/api_config/api.dockerfile .