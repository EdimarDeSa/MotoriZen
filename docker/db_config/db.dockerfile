# syntax = docker/dockerfile:1.4

FROM postgres:17.4-alpine

# Copia scripts de init
COPY docker/db_config/init_sql /docker-entrypoint-initdb.d/

# Corrige permissões para que o user postgres consiga escrever
RUN chmod -R 644 /docker-entrypoint-initdb.d/*.sql \
    && chmod +x /docker-entrypoint-initdb.d/*.sh \
    && chown -R postgres:postgres /docker-entrypoint-initdb.d

EXPOSE 5432
