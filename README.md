
# Monitor fromedwin

This project provide a no code Prometheus setup for instance down monitoring


## Installation

[Docker](https://www.docker.com/) and [Docker-compose](https://docs.docker.com/compose/) are required to run this project.
## Run Locally

Clone the project

```bash
  git clone https://github.com/fromedwin/monitor.git
```

Go to the project directory

```bash
  cd monitor
```

Start the server

```bash
  ./run.sh
```

Create a superuser

```bash
  docker exec -u root -t -i monitor_django_1 python3 manage.py createsuperuser
```

  
## Environment Variables

No variables are required to run locally, but might be needed to configure your production environment

You will need to add the following environment variables to your `.env` file

`PORT` *(default: 8000)*

`PORT_HTTPS` *(default: 8443)*

`NGINX` nginx config folder used on start *(default: local)*

`MAIL` email shared with letsencrypt to register SSL certificate

`STAGING` set to 1 if you're testing your setup to avoid hitting request limits *(default: 1)*

`DOMAIN` url used to generate letsencrypt SSL certificate and access the application

`DJANGO_SECRET_KEY` secret key used by django's session

`WEBAUTH_USERNAME` username to protect none public access

`WEBAUTH_PASSWORD` password to protect none public access

`ALERT_MANAGER_PROTOCOL` http or https used to reach alertmanager

`ALERT_MANAGER_PORT` port number used to reach alertmanager *(default: 443)*

  
## Feedback

If you have any feedback, please reach out to us at fromedwin@sebastienbarbier.com

  
## License

[MIT](https://choosealicense.com/licenses/mit/)

