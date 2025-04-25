#!/bin/bash

: "${MOTORIZEN_USER:?MOTORIZEN_USER não definido}"
: "${MOTORIZEN_PASS:?MOTORIZEN_PASS não definido}"
: "${KC_DB_USER:?KC_DB_USER não definido}"
: "${KC_DB_PASS:?KC_DB_PASS não definido}"

# Gera um SQL com os valores do .env (que são passados no container)
cat <<EOF > /docker-entrypoint-initdb.d/01_setup_users.sql
DO
\$BODY\$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = '$MOTORIZEN_USER') THEN

      CREATE ROLE $MOTORIZEN_USER WITH LOGIN PASSWORD '${MOTORIZEN_PASS}';
      ALTER ROLE $MOTORIZEN_USER CREATEDB;
   END IF;

   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = '$KC_DB_USER') THEN

      CREATE ROLE $KC_DB_USER WITH LOGIN PASSWORD '${KC_DB_PASS}';
   END IF;
END
\$BODY\$;
EOF

psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -f /docker-entrypoint-initdb.d/01_setup_users.sql
