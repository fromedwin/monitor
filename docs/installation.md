# Installation

```bash
python3 -m venv apps
source apps/bin/activate
pip install -r requirements.txt

# Generate random SECRET_KEY and inject in .env file
SECRET_KEY=$(LC_CTYPE=C tr -dc 'a-zA-Z0-9' < /dev/urandom | head -c 32)
echo "SECRET_KEY=$SECRET_KEY" >> .env

# Create superuser to access django admin panel
python django/monitor/manage.py createsuperuser

python django/monitor/manage.py migrate
python django/monitor/manage.py tailwind install
```

## Developpment mode

Run both command in parallel

```bash
python django/monitor/manage.py runserver
python django/monitor/manage.py tailwind start
```

