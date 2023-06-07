#!/bin/sh

#python manage.py collectstatic --noinput
python manage.py migrate

gunicorn api.wsgi --pythonpath="/src/api," --bind 0.0.0.0:${API_PORT} -w 4
