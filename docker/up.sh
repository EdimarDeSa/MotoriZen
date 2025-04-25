#! /bin/bash

echo "Iniciando o docker compose"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"

"$SCRIPT_DIR/down.sh"

docker compose -f "$SCRIPT_DIR/compose.yaml" up -d --build
