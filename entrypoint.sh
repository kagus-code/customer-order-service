#!/bin/sh

# Exit if any command fails
set -e

echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

echo "Starting  server..."
python manage.py runserver 0.0.0.0:3016

