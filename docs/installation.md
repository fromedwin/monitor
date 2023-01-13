# Installation

```bash
# Create a virtual environment and activate it
python3 -m venv apps
source apps/bin/activate

# Install the necessary packages
pip install -r requirements.txt

# Generate a random SECRET_KEY and add it to the .env file
SECRET_KEY=$(LC_CTYPE=C tr -dc 'a-zA-Z0-9' < /dev/urandom | head -c 32)
echo "SECRET_KEY=$SECRET_KEY" >> .env

# Create a superuser to access the Django admin panel
python django/manage.py createsuperuser

# Perform the necessary database migrations
python django/manage.py migrate

# Install tailwind
python django/manage.py tailwind install

```

## Development mode

To run the system in development mode, executed simultaneously in separate terminal windows or tabs the following commands:

```bash
# Start the Django development server
python django/manage.py runserver

# Start the tailwind process 
python django/manage.py tailwind start
```

The first command `python django/manage.py runserver` is used to **start the Django development server**. This command starts the web server on the localhost and a default port *(8000)* and allows developers to test and debug their code on their local machine.

The second command `python django/manage.py tailwind start` is used to **start the tailwind process**, it is a development utility that watches your CSS files for changes and automatically rebuilds your CSS as you work on your project. It is a helpful tool for developers to quickly test and iterate on their CSS.

---

With the development server running, the web interface can be accessed at [http://localhost:8000](http://localhost:8000), although additional configuration may be required as described the next section.
