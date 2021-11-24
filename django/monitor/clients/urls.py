from django.urls import path

from django.conf.urls import include
from rest_framework import routers
from clients.views import prometheus, register, heartbeat, alerts

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('prometheus/<uuid:id>/', prometheus),
    path('register', register),
    path('heartbeat/<uuid:id>/', heartbeat),
    path('alerts/<uuid:id>/', alerts),
]