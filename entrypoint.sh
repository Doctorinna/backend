#!/bin/bash

sleep 10
celery -A backend worker -l INFO --detach

sleep 5
python manage.py makemigrations
python manage.py migrate

DJANGO_SUPERUSER_PASSWORD="$ADMIN_PASSWORD" python manage.py createsuperuser --username "$ADMIN_USERNAME" --email "$ADMIN_EMAIL" --noinput

python manage.py collectstatic --noinput

gunicorn backend.wsgi:application --workers=2 --bind :8000
