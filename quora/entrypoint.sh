#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input


gunicorn quora.wsgi:application -w 8 --bind 0.0.0.0:8003


