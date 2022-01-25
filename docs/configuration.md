# Configuration

## How to configure

All variables have a **default value** and probably **won't need to be configured** to **run locally**.

If needed, you can **create a `.env` file** within the **root folder** and set then manually. You will need to **restart docker** images to apply them.

For **production** instance, define them directly within your **hosting platform**. 

```{warning}
Environment variables might contain **sensitive informations** and **compromise security**, make sure to **keep those values secures**.
```

## List of all configurations

### HTTP ports

Nginx listen to HTTP request. On dev mode your might keep the default value but will need on production.

`PORT` *(default: 8000, 80 with -prod)*.

`PORT_HTTPS` *(default: 8443, 443 with -prod)*.

### Contact email address

`MAIL` email shared with letsencrypt to register SSL certificate.

### Certbot https generation

`CERTBOT_STAGING` set to 1 if you're testing your setup to avoid hitting request limits *(default: 1, 0 or 1)*.

`DOMAIN` domain url used for generate the https certificate, and set within django settings.py allowed_url.  *(eg: status.fromedwin.com)*.

### Django Secret key

`DJANGO_SECRET_KEY` secret key used by django's session.

### WebAuth credentials

`WEBAUTH_USERNAME` username to protect none public access.

`WEBAUTH_PASSWORD` password to protect none public access.

### Alert Manager

`ALERT_MANAGER_PROTOCOL` http or https used to reach alertmanager *(default: http, https with -prod, http or https)*.

`ALERT_MANAGER_PORT` port number used to reach alertmanager *(default: `PORT`, `PORT_HTTPS` with -prod)*.

### Debug mode

`DEBUG` Set debug mode within django project *(default: True, False with -prod, False or True)*.
