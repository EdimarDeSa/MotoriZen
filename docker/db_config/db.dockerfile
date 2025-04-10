# syntax = docker/dockerfile:1.4

# Build stage
FROM postgres:16

# Create directory for custom configuration
RUN mkdir -p /docker-entrypoint-initdb.d && \
    chown -R postgres:postgres /docker-entrypoint-initdb.d/

# Copy custom initialization scripts
COPY docker/db_config/init_sql /docker-entrypoint-initdb.d/

# Defina permissões adequadas (644 para SQL, 755 para SH)
RUN chmod -R 644 /docker-entrypoint-initdb.d/*.sql && \
    chown -R postgres:postgres /docker-entrypoint-initdb.d

# Expose port
EXPOSE 5432
