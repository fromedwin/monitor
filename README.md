# Status From Edwin

This project provide an **out of the box** **highly opinionated implementation** of open-source **monitoring tools**, unified as a **no code web interface**.

Metrics are focused on **availability**, with future integration for **performance**, **statistics**, **budget**, and **energy consumption**.

[![Build action badge](https://github.com/fromedwin/monitor/actions/workflows/django.yml/badge.svg?branch=main)](https://github.com/fromedwin/monitor/actions/) [![Documentation Status](https://readthedocs.org/projects/fromedwin-monitor/badge/?version=latest)](https://fromedwin-monitor.readthedocs.io/en/latest/?badge=latest) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/fromedwin/monitor/blob/main/LICENSE)

## Installation

```bash
python3 -m venv apps
source apps/bin/activate
pip install -r django/requirements.txt

# Generate random SECRET_KEY and inject in .env file
SECRET_KEY=$(LC_CTYPE=C tr -dc 'a-zA-Z0-9' < /dev/urandom | head -c 32)
echo "SECRET_KEY=$SECRET_KEY" >> .env

# Create superuser to access django admin panel
python django/manage.py createsuperuser

python django/manage.py migrate
python django/manage.py tailwind install
```

## Developpment mode

### Django development server

Start the development server by running the following command:

```bash
python django/manage.py runserver
```

To enable styling and hot-reload, run in parallel the following command:

```bash
python django/manage.py tailwind start
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
