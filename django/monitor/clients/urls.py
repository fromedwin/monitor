from django.urls import path

from django.conf.urls import include
from rest_framework import routers
from clients.views import AlertsConfigViewSet, prometheus, register, heartbeat

router = routers.DefaultRouter()
router.register(r'alerts', AlertsConfigViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('prometheus/<uuid:id>/', prometheus),
    path('register', register),
    path('heartbeat/<uuid:id>/', heartbeat),
]