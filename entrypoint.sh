#!/bin/sh

# Exit if any command fails
set -e

echo "Running migrations..."
python manage.py migrate --noinput


echo "Starting Gunicorn server..."
exec gunicorn customer_order_service.wsgi:application --bind 0.0.0.0:3016 --workers 4
