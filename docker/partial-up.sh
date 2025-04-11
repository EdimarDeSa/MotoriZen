
echo "Iniciando o docker-compose"
docker-compose -f docker/compose.yaml up postgres redis keycloak -d