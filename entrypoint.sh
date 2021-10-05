#!/bin/bash

sleep 10

python manage.py makemigrations
python manage.py migrate

python manage.py populate

DJANGO_SUPERUSER_PASSWORD="$ADMIN_PASSWORD" python manage.py createsuperuser --username "$ADMIN_USERNAME" --email "$ADMIN_EMAIL" --noinput

python manage.py collectstatic --noinput

gunicorn backend.wsgi:application --bind :8000