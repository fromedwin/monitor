touch .env
touch django/monitor/.env

docker-compose up -d

# If ./.env file exist, we export variables to current system to display later
if [ -f .env ]; then
  export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)
fi

echo "Access fromedwin/monitor at localhost:$PORT"