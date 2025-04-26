#!/bin/sh

: "${REDIS_USER:?REDIS_USER must be set}"
: "${REDIS_PASSWORD:?REDIS_PASSWORD must be set}"
: "${REDIS_PORT:?REDIS_PORT must be set}"

# Start Redis with the configuration
cat > /tmp/redis.conf <<EOF
# Redis Configuration
always-show-logo yes

# Network
bind 0.0.0.0
port $REDIS_PORT
protected-mode yes

# Security
user default off
user ${REDIS_USER} on >${REDIS_PASSWORD} allcommands allkeys

# Memory Management
maxmemory 256mb
maxmemory-policy allkeys-lru

# Persistence
dir /data
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite yes
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
databases 7

# Logging
loglevel notice
logfile ""

# Performance
tcp-keepalive 300
timeout 0
tcp-backlog 511

# Snapshotting
save 900 1
save 300 10
save 60 10000
stop-writes-on-bgsave-error yes
rdbcompression yes
rdbchecksum yes
dbfilename dump.rdb

# Client Connection Settings
maxclients 20

# Slow Log
slowlog-log-slower-than 10000
slowlog-max-len 128

# Latency Monitor
latency-monitor-threshold 100

EOF

exec redis-server /tmp/redis.conf