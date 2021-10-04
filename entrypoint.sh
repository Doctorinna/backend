#!/bin/bash

python manage.py makemigrations
python manage.py migrate

DJANGO_SUPERUSER_PASSWORD=$ADMIN_PASSWORD python manage.py createsuperuser --username $ADMIN_USERNAME --email $ADMIN_EMAIL --noinput

python manage.py collectstatic --noinput

gunicorn backend.wsgi:application --bind 0.0.0.0:8000