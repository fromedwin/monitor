# Deployment

Follow the same process as describe within the [installation page](./installation).

## Configure GeoLite2

You need to register and request an authentication key to automatically download the Geomind database from maxming.

Registration can be done on [maxmind website](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data?lang=en).

Then define your License key as the environment variable `MAXMIND_KEY` (can be one within a `.env` file).

```bash
./install.sh
```

## Generate SSL certificate

```bash
./run -prod -cert
```

## Run

```bash
./run.sh -prod
```