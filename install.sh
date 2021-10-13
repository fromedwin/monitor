#!/bin/bash

# If ./.env file exist, we export variables to current system to display later
if [ -f .env ]; then
  export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)
fi

cd nginx

mkdir -p 'geolite'

wget "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key=$MAXMIND_KEY&suffix=tar.gz" -O "./geolite/GeoLite2-City.tar.gz"

wget "https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-Country&license_key=$MAXMIND_KEY&suffix=tar.gz" -O "./geolite/GeoLite2-Country.tar.gz"

cd geolite

tar -xf "./GeoLite2-City.tar.gz"
tar -xf "./GeoLite2-Country.tar.gz"

rm "./GeoLite2-City.tar.gz"
rm "./GeoLite2-Country.tar.gz"

find . -iname "GeoLite2-City.mmdb" -exec mv {} . \;
find . -iname "GeoLite2-Country.mmdb" -exec mv {} . \;

# docker-compose pull