touch .env
touch django/monitor/.env

# If ./.env file exist, we export variables to current system to display later
if [ -f .env ]; then
  export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)
fi

echo "Loading nginx/$NGINX files"

docker-compose up -d

echo "Access fromedwin/monitor at localhost:$PORT"