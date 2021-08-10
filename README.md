# Monitor

## Configure

Define basic authentication credentials for NGINX using apache2-utils. Verify that apache2-utils (Debian, Ubuntu) or httpd-tools (RHEL/CentOS/Oracle Linux) is installed. (See [documentation](https://docs.nginx.com/nginx/admin-guide/security-controls/configuring-http-basic-authentication/) for details)

```
$> sudo htpasswd -cm .htpasswd user1
$> sudo htpasswd .htpasswd user2
```

You can confirm that the file contains paired usernames and encrypted passwords:

```
$ cat .htpasswd
user1:$apr1$/woC1jnP$KAh0SsVn5qeSMjTtn0E9Q0
user2:$apr1$QdR8fNLT$vbCEEzDj7LyqCMyNpSoBh/
user3:$apr1$Mr5A0e.U$0j39Hp5FfxRkneklXaMrr/
```

### Configure Pagerduty

Uncomment the pagerduty_configs from receivers :
```
#  pagerduty_configs:
#  - routing_key: 'YOU_CODE_GOES_HERE'
````

## Create django .env

```
$> touch django/monitor/.env
```

Add a SECRET_KEY value within the .env file you just created

```
 SECRET_KEY="abcd"
```

## Create nginx golder in data/log

```
$> mkdir data/log/nginx
```

## Run

```
$> docker-compose up
```
