# Configuration

It is considered best practice to store sensitive information such as access keys, secret keys, and other credentials as **environment variables**. This is because environment variables are stored outside of the codebase and are not committed to version control, making them less likely to be exposed in the event of a security breach.

```{warning}
When using environment variables, it's important to make sure that they are **properly protected and only accessible by the necessary parties**.
```

This project uses a local `.env` file that is loaded on startup **for local development** to store sensitive configuration values.

## List of variables

| Configuration value | Description |
| --- | --- |
| `SECRET_KEY` | The secret key used for signing cookies |
| `DOMAIN` | The domain used to access the web interface (default `localhost`) |
| `PORT` | The port used to access the web interface (default `8000`)|
| `DEBUG` | The debug mode value (default `1`) |
| `DATABASE_URL` *(optional)* | URL of the database that the system will connect to. (default `sqlite3`) |

## For deployment only

`STORAGE` variable is used to specify the storage method used for static files. The default value is set to S3, which means that the system is configured to use an S3-like bucket to store the static files.'

| Configuration value | Description |
| --- | --- |
| `STORAGE` | The storage method used |
| `AWS_ACCESS_KEY_ID` | The access key ID used for AWS S3 storage |
| `AWS_SECRET_ACCESS_KEY` | The secret access key used for AWS S3 storage |
| `AWS_S3_CUSTOM_DOMAIN` | The custom domain used for AWS S3 storage |
| `AWS_STORAGE_BUCKET_NAME` | The bucket name used for AWS S3 storage |

