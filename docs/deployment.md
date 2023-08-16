# Deployment

The deployment process for FromEdwin involves the following steps:

```bash
# Create a virtual environment
python3 -m venv apps
source apps/bin/activate

# Install the required dependencies
pip install -r requirements.txt

#Initialize and build the Tailwind CSS framework
python django/manage.py tailwind install
python django/manage.py tailwind build

#Run database migrations
python django/manage.py migrate

# Collect static files
python django/manage.py collectstatic --no-input
```

Once these steps are completed, you can use a **production-ready web server** *like Gunicorn* to start the `core.wsgi:application` Python code and serve the application to users.

```bash
gunicorn core.wsgi:application
```

It is also important to note that the environment variables should be set before running the web server.

## Static files

`STORAGE` variable is used to specify the **storage method used for static files**. The default value is set to `S3`, which means that the system is configured to use an **S3-like bucket** to store the static files.

`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_S3_CUSTOM_DOMAIN`, and `AWS_STORAGE_BUCKET_NAME` are variables used to **configure the connection** to an S3-like bucket for storing static files.

These variables should be set in production environment, as the default configuration uses the local filesystem for storage which is not suitable for production.

## Deployment with Github Actions

A detailed description of the deployment process for FromEdwin, including all the necessary steps and commands, can be found within the [Github Actions workflow](https://github.com/fromedwin/monitor/blob/main/.github/workflows/django.yml) of the main repository. 

This should provide a clear understanding of how the system is currently deployed and can serve as a reference for anyone interested in setting up their own instance.
