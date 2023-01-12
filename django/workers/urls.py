from django.urls import path

from django.conf.urls import include
from workers.views import prometheus, alertmanager, register, heartbeat, alerts


urlpatterns = [
    path('register', register),
    path('heartbeat/<uuid:id>/', heartbeat),
    # Access custom configuration files
    path('prometheus/<uuid:id>/', prometheus),
    path('alertmanager/<uuid:id>/', alertmanager),
    path('alerts/<uuid:id>/', alerts),
]