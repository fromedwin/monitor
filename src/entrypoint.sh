#!/bin/sh

if [ "$DJANGO_SETTINGS_MODULE" = "fromedwin.settings.prod" ]; then
  echo "Production mode detected. Exiting immediately."
  exit 0
fi


if [ -z "$SECRET_KEY" ]; then
  echo "No SECRET_KEY found. Generating a new one..."
  export SECRET_KEY=$(tr -dc 'a-z0-9!@#$%^&*(-_=+)' < /dev/urandom | head -c50)
  echo "SECRET_KEY generated successfully."
fi

export COMPRESS_OFFLINE=True

cd /app/src

python manage.py compilescss
python manage.py collectstatic --noinput
python manage.py migrate

python manage.py tailwind install
python manage.py tailwind start &


# gunicorn fromedwin.wsgi:application --bind 0.0.0.0:${PORT:-8000}
python manage.py runserver 0.0.0.0:${PORT:-8000}