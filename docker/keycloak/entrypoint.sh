#!/bin/bash

: "${KC_USER:?KC_USER must be set}"
: "${KC_PASSWORD:?KC_PASSWORD must be set}"
: "${KC_CLIENT_ID:?KC_CLIENT_ID must be set}"
: "${KC_CLIENT_SECRET_KEY:?KC_CLIENT_SECRET_KEY must be set}"
: "${KC_REALM:?KC_REALM must be set}"

: "${KC_DB:?KC_DB must be set}"
: "${KC_DB_URL:?KC_DB_URL must be set}"
: "${KC_DB_USERNAME:?KC_DB_USERNAME must be set}"
: "${KC_DB_PASSWORD:?KC_DB_PASSWORD must be set}"

: "${KC_SECRET_DATA_VALUE:?KC_SECRET_DATA_VALUE must be set}"
: "${KC_SECRET_DATA_SALT:?KC_SECRET_DATA_SALT must be set}"

: "${KC_HEALTH_ENABLED:?KC_HEALTH_ENABLED must be set}"
: "${KC_METRICS_ENABLED:?KC_METRICS_ENABLED must be set}"


# # Cria pasta para imports
mkdir -p /opt/keycloak/data/import

# Create reaml to be imported from a template
sed -e "s/{{KC_CLIENT_ID}}/${KC_CLIENT_ID}/g" \
    -e "s/{{KC_CLIENT_SECRET_KEY}}/${KC_CLIENT_SECRET_KEY}/g" \
    -e "s/{{KC_REALM}}/${KC_REALM}/g" \
    /opt/keycloak/data/json_reaml_templates/motorizen-realm.json > /opt/keycloak/data/import/motorizen-realm.json

sed -e "s/{{KC_USER}}/${KC_USER}/g" \
    -e "s/{{KC_CLIENT_ID}}/${KC_CLIENT_ID}/g" \
    -e "s/{{KC_REALM}}/${KC_REALM}/g" \
    -e "s/{{KC_SECRET_DATA_VALUE}}/${KC_SECRET_DATA_VALUE}/g" \
    -e "s/{{KC_SECRET_DATA_SALT}}/${KC_SECRET_DATA_SALT}/g" \
    /opt/keycloak/data/json_reaml_templates/motorizen-users-0.json > /opt/keycloak/data/import/motorizen-users-0.json


# Start Keycloak in the background
/opt/keycloak/bin/kc.sh \
    start-dev \
    --import-realm