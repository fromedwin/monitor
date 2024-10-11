# app_name/tasks.py
from celery import shared_task

@shared_task
def my_periodic_task():
    print("This task runs every 10 seconds.")