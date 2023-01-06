# Configuration

## How to configure

All variables have a **default value** and probably **won't need to be configured** to **run locally**.

If needed, you can **create a `.env` file** within the **root folder** and set then manually. You will need to **restart docker** images to apply them.

For **production** instance, define them directly within your **hosting platform**. 

```{warning}
Environment variables might contain **sensitive informations** and **compromise security**, make sure to **keep those values secures**.
```

## List of all configurations

### Contact email address

`MAIL` email shared with letsencrypt to register SSL certificate.

### Django Secret key

`DJANGO_SECRET_KEY` secret key used by django's session.

### Debug mode

`DEBUG` Set debug mode within django project *(default: True, False with -prod, False or True)*.
