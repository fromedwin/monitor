# Getting started

**This documentation will assume you are familiar with your system terminal**, running **git**, **[docker](https://www.docker.com/)**, and **[docker-compose](https://docs.docker.com/compose/)** instruction. Also make sure those are **installed on your machine**.

Instructions have been **tested on MacOS and Linux**.

## Download the project

Use **git** to clone locally the main repository.

```bash
git clone https://github.com/fromedwin/monitor.git
```

```{note}
Release notes and versioning will be **implemented soon**. Until then we recommand to **only run the latest version**.
```

## Starting locally

Start a local dev server with

```bash
./run.sh 
# use ./run.sh -d to run in background
```

*Troubleshooting, you might require to install `apache2-utils` package to use the `htpasswd` cmd.*

You can now use **use your browser** to access the following application:

- [localhost:8000](http://localhost:8000): main home page
- [localhost:8000/admin](http://localhost:8000/admin): django administration page
- [localhost:8000/docs/](http://localhost:8000/docs/): sphinx documentation
- [localhost:8000/grafana/](http://localhost:8000/grafana/): grafana web interface

The following service is protected by a **Web authentication**. Generated **username** and **password** are **displayed in the console** when first running the run script. They can be [configured](configuration) to be **static**.

- [localhost:8000/alertmanager/](http://localhost:8000/alertmanager/): alertmanager web interface

## Create a superuser

A **django superuser account** will be needed to configure the [oAuth authentication](authentication).

```bash
docker exec -u root -t -i monitor_django python3 manage.py createsuperuser
```

**Follow the instructions**, then try using the user account within the  [django administration page](http://localhost:8000/admin/login/). *You can always rerun this command to create a new user in case you are locked outside of the application.*

## Other commands

### Stop all services

```bash
./stop.sh
```

### Update and migrate local instance

After using `git pull` to fetch **the latest version**, run the following command.

```bash
./update.sh
```

