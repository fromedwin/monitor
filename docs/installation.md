# Installation

## Docker

[Docker](https://www.docker.com/) and [Docker-compose](https://docs.docker.com/compose/) are required to run this project.

### Run Locally

Clone the project

```bash
  git clone https://github.com/fromedwin/monitor.git
```

Go to the project directory

```bash
  cd monitor
```

Install dependencies

```bash
  ./install.sh
```

Start the server

```bash
  ./run.sh
```

Create a superuser

```bash
  docker exec -u root -t -i monitor_django python3 manage.py createsuperuser
```