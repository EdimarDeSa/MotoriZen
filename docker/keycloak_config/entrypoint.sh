#!/bin/bash

# Start Keycloak in the background
/opt/keycloak/bin/kc.sh start-dev &

# Run the configuration script
/configure-keycloak.sh

# Keep the container running
tail -f /dev/null