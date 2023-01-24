from django.urls import path

from django.conf.urls import include
from workers.views import prometheus, alertmanager, register, heartbeat, alerts


urlpatterns = [
    # Worker register and receive uuid to identify
    path('register', register),
    # Worker update it status as online every x minutes
    path('heartbeat/<uuid:id>/', heartbeat),

    # """"
    # Access custom configuration files based on user data
    # """"
    # Prometheus configuration file
    path('prometheus/<uuid:id>/', prometheus),
    # Alertmanager with differet pagerDuty data
    path('alertmanager/<uuid:id>/', alertmanager),
    # Alerts triggered
    path('alerts/<uuid:id>/', alerts),
]
