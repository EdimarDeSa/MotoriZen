#!/bin/bash

# Wait for Keycloak to be ready
until curl -s http://localhost:8080/health/ready; do
    echo "Waiting for Keycloak to be ready..."
    sleep 5
done

# Get admin token
ADMIN_TOKEN=$(curl -X POST http://localhost:8080/realms/master/protocol/openid-connect/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=$' \
  -d 'password=admin' \
  -d 'grant_type=password' \
  -d 'client_id=admin-cli' | jq -r '.access_token')

# Create realm
curl -X POST http://localhost:8080/admin/realms \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "realm": "motorizen",
    "enabled": true,
    "displayName": "MotoriZen"
  }'

# Create user
curl -X POST http://localhost:8080/admin/realms/motorizen/users \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "username": "support",
    "enabled": true,
    "credentials": [{
      "type": "password",
      "value": "123",
      "temporary": false
    }]
  }'

# Create client
curl -X POST http://localhost:8080/admin/realms/motorizen/clients \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{
    "clientId": "api-client",
    "enabled": true,
    "publicClient": false,
    "redirectUris": ["*"],
    "webOrigins": ["*"],
    "directAccessGrantsEnabled": true,
    "serviceAccountsEnabled": true
  }'

echo "Keycloak configuration completed!" 