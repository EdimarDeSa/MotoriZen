#! /bin/bash

echo "Parando o docker-compose"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"

docker compose -f $SCRIPT_DIR/compose.yaml down --remove-orphans

docker volume rm motorizen_redis_volume
docker container rm $(docker ps -aq)
