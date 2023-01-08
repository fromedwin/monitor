from django.urls import path

from django.conf.urls import include
from rest_framework import routers
from clients.views import prometheus, alertmanager, register, heartbeat, alerts

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('register', register),
    path('heartbeat/<uuid:id>/', heartbeat),
    # Access custom configuration files
    path('prometheus/<uuid:id>/', prometheus),
    path('alertmanager/<uuid:id>/', alertmanager),
    path('alerts/<uuid:id>/', alerts),
]