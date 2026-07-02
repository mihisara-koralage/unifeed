#!/bin/bash
set -e

echo "Running collectstatic..."
python manage.py collectstatic --noinput --clear

echo "Running migrations..."
python manage.py migrate

echo "Starting Daphne..."
daphne -b 0.0.0.0 -p $PORT config.asgi:application