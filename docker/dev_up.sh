#! /bin/bash

echo "Iniciando o docker compose em modo desenvolvimento"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"

docker compose -f "$SCRIPT_DIR/compose.yaml" up -d --build postgres redis keycloak
