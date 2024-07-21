#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Run migrations
python manage.py migrate --no-input

# Ensure the celerybeat-schedule file exists
touch /home/app/web/celerybeat-schedule
chown app:app /home/app/web/celerybeat-schedule

# Collect static files
python manage.py collectstatic --no-input

# Set PYTHONPATH
export PYTHONPATH=/home/app/web

# Start Gunicorn
exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000
