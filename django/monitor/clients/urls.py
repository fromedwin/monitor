from django.urls import path

from django.conf.urls import include
from rest_framework import routers
from clients.views import AlertsConfigViewSet, PrometheusConfigViewSet

router = routers.DefaultRouter()
router.register(r'alerts', AlertsConfigViewSet)
router.register(r'prometheus', PrometheusConfigViewSet)

urlpatterns = [
    path('', include(router.urls)),
]