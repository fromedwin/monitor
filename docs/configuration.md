# Configuration

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

`DEBUG` Set debug mode within django project *(default: False)*
