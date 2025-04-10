#! /bin/bash

# Run docker keycloak
echo "==================== Running docker keycloak ===================="
docker/keycloak_config/run.sh

# Run docker api
echo "====================== Running docker api ======================"
docker/api_config/run.sh

# Run docker redis
echo "===================== Running docker redis ====================="
docker/redis_config/run.sh

# Run docker db
echo "======================= Running docker db ======================="
docker/db_config/run.sh
