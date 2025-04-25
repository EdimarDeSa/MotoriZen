#! /bin/bash

# Build docker motorizen_db
docker/db_config/stop.sh
docker image rm motorizen:db
docker build -t motorizen:db -f docker/db_config/db.dockerfile .