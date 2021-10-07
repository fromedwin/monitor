#!/bin/bash

touch django/monitor/.env

# If ./.env file exist, we export variables to current system to display later
if [ -f .env ]; then
  export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)
fi

# Set default nginx files as local
if [[ -z "${NGINX}" ]]; then export NGINX="local"
fi
# Set default port to access dashboard
if [[ -z "${PORT}" ]]; then export PORT=8000
fi
# Set default username for web auth
if [[ -z "${WEBAUTH_USERNAME}" ]]; then export WEBAUTH_USERNAME=$(openssl rand -base64 12)
fi
# Set default password for webauth
if [[ -z "${WEBAUTH_PASSWORD}" ]]; then export WEBAUTH_PASSWORD=$(openssl rand -base64 12)
fi
# Set django Secret key on start
if [[ -z "${DJANGO_SECRET_KEY}" ]]; then export DJANGO_SECRET_KEY=$(openssl rand -base64 24)
fi
# Set domain to share and use to reach Django app
if [[ -z "${DOMAIN}" ]]; then export DOMAIN="host.docker.internal"
fi

# GENERATE PASSWORD
htpasswd -cmb .htpasswd $WEBAUTH_USERNAME $WEBAUTH_PASSWORD

# Create shared volume between django and alertmanager
mkdir -p alertmanager/shared && cp alertmanager/alertmanager.yml alertmanager/shared/alertmanager.yml

echo "Loading nginx/$NGINX files"

if [[ $@ == *"-d"* ]]; then
  docker-compose up -d

  # IF load-config.py return code 0
  if [ $? -ne 0 ]; then
    echo "❌ Docker might not be running."
    exit
  fi
  
  echo "✅ Access fromedwin/monitor at localhost:$PORT"

else
  docker-compose up
fi

