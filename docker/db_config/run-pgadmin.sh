#! /bin/bash

# Run docker motorizen_db
docker container stop pgadmin
docker container rm pgadmin
docker container run -d --rm \
--name pgadmin \
-p 5050:5050 \
--network=postgres_network \
--hostname=pgadmin \
-e PGADMIN_DEFAULT_EMAIL=support@efscode.com.br \
-e PGADMIN_DEFAULT_PASSWORD=motorizen \
-e PGADMIN_LISTEN_PORT=5050 \
-e PGADMIN_CONFIG_SERVER_MODE=false \
-e PGADMIN_CONFIG_PATH=/pgadmin4/servers.json \
-v pgadmin_data:/pgadmin4/servers.json \
docker.io/dpage/pgadmin4:latest