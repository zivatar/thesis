#!/usr/bin/env bash
#sleep 10
#python3 manage.py migrate
#python3 manage.py runserver 0.0.0.0:8000
gunicorn --timeout=30 --workers=2 --bind 0.0.0.0:8000 django_app.wsgi:application
