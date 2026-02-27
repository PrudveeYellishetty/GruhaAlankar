#!/bin/bash
set -e

echo "=== GruhaAlankar Startup ==="

# Pull models from GitHub
python3 startup.py

# Start gunicorn
echo "Starting Flask server..."
exec gunicorn --bind 0.0.0.0:5000 \
  --workers 4 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  "app:create_app()"
