# Task manager

## Scheduler

Scheduler run tasks at regular interval. It run within Django and can use its ORM but do not have access to its database. 

It mostly fetch data and trigger more tasks for workers like queue deprecated report to refresh.

## Worker

This is Django code listenning to rabbitMQ and running code as worker. It does not have access to database and run API calls to fetch data.