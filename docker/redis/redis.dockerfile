# syntax = docker/dockerfile:1.4

FROM redis:alpine

# Set environment variables
ENV REDIS_PORT=6379

# Create directory for custom configuration
RUN mkdir -p /etc/redis

# Copy custom Redis configuration and entrypoint script
COPY docker/redis_config/redis.conf /etc/redis/redis.conf
COPY docker/redis_config/entrypoint.sh /entrypoint.sh

# Make entrypoint script executable and set proper permissions
RUN chmod +x /entrypoint.sh && \
    chown -R redis:redis /etc/redis && \
    chmod 755 /etc/redis && \
    chmod 644 /etc/redis/redis.conf

# Create directory for Redis data
RUN mkdir -p /data && chown -R redis:redis /data

# Switch to non-root user
USER redis

# Expose Redis port
EXPOSE ${REDIS_PORT}

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]
