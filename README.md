# Monitor

Monitor is a django application to configure a set of docker images and provide prometheus metrics as no or low code.

## Run

```bash
./run.sh
./run.sh -d # Run locally as deamon
```

Default UI is available

## Stop

```bash
./stop.sh
```

## Customise credential for web auth

```
sudo htpasswd .htpasswd user2
``` 

# Frequently Asked Questions

## no such table: django_session

Run `docker exec -u root -t -i monitor_django_1 python3 manage.py migrate`

## Create super user

Run `docker exec -u root -t -i monitor_django_1 python3 manage.py createsuperuser`

## Install python dependancies

Run `apk update && apk add alpine-sdk gcc musl-dev python3-dev libffi-dev openssl-dev`