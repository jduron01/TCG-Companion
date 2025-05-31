#!/bin/bash

echo "Starting Gunicorn..."
gunicorn tcg_companion.wsgi:application --bind 127.0.0.1:8000 --workers 8 --threads 4 &

echo "Starting nginx..."
nginx -g "daemon off;"

# python manage.py runserver 0.0.0.0:80