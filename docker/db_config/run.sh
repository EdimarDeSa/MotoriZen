#! /bin/bash

# Run docker motorizen_db
docker/db_config/stop.sh
docker container run -d --rm \
--name=motorizen_db \
-p 5432:5432 \
--network=postgres_network \
--hostname=motorizen_db \
--env-file=docker/db_config/db.env \
-v motorizen_db:/var/lib/postgresql/data \
motorizen:db
