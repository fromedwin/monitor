# Installation

## Run locally

### Clone git repository

Create a folder where to run your project and clone our main repository.

```bash
mkdir monitor
cd monitor
git clone https://github.com/fromedwin/monitor.git
```

### Configure GeoLite2

You need to register and request an authentication key to automatically download the Geomind database from maxming.

Registration can be done on [maxmind website](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data?lang=en).

Then define your License key as the environment variable `MAXMIND_KEY` (can be one within a `.env` file).

### Install and build docker

[Docker](https://www.docker.com/) and [Docker-compose](https://docs.docker.com/compose/) are required to run this project.

```bash
./install.sh
```

### Run locally

Start a local dev server with

```bash
  ./run.sh
```

Server can be start in background using `-d` parameter. 

Open `http://localhost:8000` to access your local instance. 

### Create a superuser account

Create a superuser

```bash
  docker exec -u root -t -i monitor_django python3 manage.py createsuperuser
```

You can now login on [localhost:8000/admin](http://localhost:8000/admin)