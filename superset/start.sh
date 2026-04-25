#!/bin/bash
# Railway-friendly Superset startup: run one-time init, then serve.
set -e

export SUPERSET_HOME="${SUPERSET_HOME:-/app/superset_home}"
mkdir -p "$SUPERSET_HOME"

# Apply/upgrade the metadata schema every boot (fast no-op if nothing to do).
superset db upgrade

# Create admin if it doesn't exist yet — Superset returns non-zero on duplicate,
# so swallow failures. After first success, subsequent boots skip cleanly.
if [ -n "$SUPERSET_ADMIN_PASSWORD" ]; then
  superset fab create-admin \
    --username "${SUPERSET_ADMIN_USERNAME:-admin}" \
    --firstname Admin \
    --lastname User \
    --email "${SUPERSET_ADMIN_EMAIL:-admin@local}" \
    --password "$SUPERSET_ADMIN_PASSWORD" \
    || echo "admin already exists, continuing"
fi

# Load example dataset the first time so the user has data to play with.
if [ ! -f "$SUPERSET_HOME/.examples_loaded" ]; then
  echo "Loading Superset example datasets + dashboards..."
  superset load-examples --force || true
  touch "$SUPERSET_HOME/.examples_loaded"
fi

# Seed role/perm defaults.
superset init

# Launch the server.
PORT="${PORT:-8088}"
exec gunicorn \
  --bind "0.0.0.0:${PORT}" \
  --access-logfile - \
  --error-logfile - \
  --workers 2 \
  --worker-class gthread \
  --threads 20 \
  --timeout 120 \
  "superset.app:create_app()"
