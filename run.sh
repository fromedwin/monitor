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

echo "Loading nginx/$NGINX files"

docker-compose up -d

echo "Access fromedwin/monitor at localhost:$PORT"