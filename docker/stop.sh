#! /bin/bash

# Stop docker api
echo "Stopping docker api"
docker/api_config/stop.sh

# Stop docker keycloak
echo "Stopping docker keycloak"
docker/keycloak_config/stop.sh

# Stop docker redis
echo "Stopping docker redis"
docker/redis_config/stop.sh

# Stop docker db
echo "Stopping docker db"
docker/db_config/stop.sh
