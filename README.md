# Status From Edwin

This project provide an **out of the box** **highly opinionated implementation** of open-source **monitoring tools**, unified as a **no code web interface**.

Metrics are focused on **availability**, with future integration for **performance**, **statistics**, **budget**, and **energy consumption**.

[![Build action badge](https://github.com/fromedwin/monitor/actions/workflows/django.yml/badge.svg?branch=main)](https://github.com/fromedwin/monitor/actions/) [![Documentation Status](https://readthedocs.org/projects/fromedwin-monitor/badge/?version=latest)](https://fromedwin-monitor.readthedocs.io/en/latest/?badge=latest) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/fromedwin/monitor/blob/main/LICENSE)

## Installation

```bash
python3 -m venv apps
source apps/bin/activate

# psycopg2 lib Apple silicon specific
# brew install openssl
# export LIBRARY_PATH=$LIBRARY_PATH:/opt/homebrew/opt/openssl/lib

pip install -r src/requirements.txt

# Generate random SECRET_KEY and inject in .env file
SECRET_KEY=$(LC_CTYPE=C tr -dc 'a-zA-Z0-9' < /dev/urandom | head -c 32)
# Or 
# SECRET_KEY=$(openssl rand -base64 64)

echo "SECRET_KEY=$SECRET_KEY" >> .env

# For development, add DEBUG=1 in .env file
# echo "DEBUG=1" >> .env

# For a first setup, run migrate and createsuperuser
python src/manage.py migrate
# Create superuser to access django admin panel (migrate first for the first setup)
python src/manage.py createsuperuser

python src/manage.py tailwind install
```

## Developpment mode

### Django development server

Start the development server by running the following command:

```bash
python src/manage.py runserver
```

To enable styling and hot-reload, run in parallel the following command:

```bash
python src/manage.py tailwind start
```

### Services

Project need a set of services like rabbitmq to run in the background. 

You can run them using the following:

```
docker-compose -f docker-compose-services.yaml up -d
```

### Scheduler

Scheduler will run periodical tasks and propagate to workers

```
cd src
python ../scheduler/start_celery_beat.py
```

or using docker

```
docker-compose -f docker-compose-scheduler.yaml up -d
```

### Worker

Worker will listen to tasks and run then individually 

```
cd src
python ../worker/start_celery_worker.py
```

or using docker

```
docker-compose -f docker-compose-worker.yaml up -d
```

## Running documentation

```bash
cd ./sphinx
pip install -r requirements.txt
sphinx-reload ../docs
```

## Env variables

`DATABASE_URL`: (optional) URL to access database

## Dependencies

- https://github.com/dvelasquez/lighthouse-viewer
