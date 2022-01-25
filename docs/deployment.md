# Deployment

Same as during the [installation](./installation) process, **download the code** on a server the follow the next few steps.

## Enable nginx geolocation

For **analytics** purpose, nginx will **assign a country** to each request based on its IP address. Such feature require the use of an external adatabase.

The company **[Maxmind](https://maxmind.com)** provide a free [GeoLite2 Geolocation Database](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data?lang=en) for such case, but require to **sign up** and **generate a license key**.

Follow the [instructions](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data?lang=en) then store the generated key within the `MAXMIND_KEY` environement variable. You can then **run** `./install.sh` to **automatically download and setup** such database.

## Generate SSL certificate

Configure a `DOMAIN` and `MAIL` to allow certbot to generate a **SSL certificate** and **enable https** requests. 
Make sure the selected domain **already redirect to the server IP**.

```bash
./run.sh -prod -cert
```

By default request will be send to the **[Staging Environment](https://letsencrypt.org/docs/staging-environment/)**. When successfully passing, set `CERTBOT_STAGING` to `0` and run again to **generate a  definitive certificate**.

## Use the *-prod* argument

To **start your production cluster**, run `./run.sh -prod`.

You can then use the same `./update.sh` or `./stop.sh` script as locally to manage your images.