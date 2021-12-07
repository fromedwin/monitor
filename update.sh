docker exec -ti monitor_django python3 manage.py migrate
docker exec -ti monitor_django python3 manage.py tailwind build
docker exec -ti monitor_django python3 manage.py collectstatic --noinput