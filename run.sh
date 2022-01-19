#!/bin/bash

touch django/monitor/.env

# If ./.env file exist, we export variables to current system to display later
if [ -f .env ]; then
  export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)
fi

# Set default port to access dashboard
if [[ -z "${PORT}" ]]; then
  if [[ $@ == *"-prod"* ]]; then
    export PORT=80
  else
    export PORT=8000
  fi
fi
# Set default https port to access dashboard
if [[ -z "${PORT_HTTPS}" ]]; then
  if [[ $@ == *"-prod"* ]]; then
    export PORT_HTTPS=443
  else
    export PORT_HTTPS=8443
  fi
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
echo "Generate user $WEBAUTH_USERNAME with password $WEBAUTH_PASSWORD"
htpasswd -cmb .htpasswd $WEBAUTH_USERNAME $WEBAUTH_PASSWORD

# Create shared volume between django and alertmanager
mkdir -p alertmanager/shared && cp alertmanager/alertmanager.yml alertmanager/shared/alertmanager.yml

if [[ $@ == *"-prod"* ]]; then

  export NGINX="production" # Will load nginx/production/*.conf files

  if [[ $DOMAIN == *"localhost"* ]]; then
    echo 'You need to define a custom domain other than localhost or host.docker.internal'
    exit
  fi

  if [[ $DOMAIN == *"host.docker.internal"* ]]; then
    echo 'You need to define a custom domain other than localhost or host.docker.internal'
    exit
  fi

  if [[ -z "${MAIL}" ]]; then 
    echo 'Defining MAIL env var is required'
    exit
  fi

  # Set STAGING to 1 if you're testing your setup to avoid hitting request limits
  if [[ -z "${STAGING}" ]]; then 
    export STAGING=0
    echo '⚠️ Running lets-encrypt staging with potential request limits'
  fi

  if [[ $@ == *"-cert"* ]]; then
    source scripts/init-letsencrypt.sh
  else
    docker-compose --profile prod up -d
  fi

else

  if [[ $@ == *"-d"* ]]; then
    docker-compose --profile dev up -d

    # IF load-config.py return code 0
    if [ $? -ne 0 ]; then
      echo "❌ Docker might not be running."
      exit
    fi

    echo "✅ Access fromedwin/monitor at localhost:$PORT"

  else
    docker-compose --profile dev up
  fi
fi
