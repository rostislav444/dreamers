#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py migrate

# change owner of celerybeat-schedule file to app user
touch /home/app/web/celerybeat-schedule
chown app:app /home/app/web/celerybeat-schedule

# change owner of static_root file to app user
touch /home/app/web/static_root
chown app:app /home/app/web/static_root

# Collect static files
python manage.py collectstatic --no-input

exec "$@"