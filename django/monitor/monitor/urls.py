"""monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf import settings
from django.conf.urls import include, url

from .views import public
from incidents.views import webhook
from health.views import healthy
from home.views import index

urlpatterns = [
    path('', index, name='index'),
    path('', include('django_prometheus.urls')),
    path('status/<int:id>/', public, name='public'),
    path('projects/', include('projects.urls')),
    path('settings/', include('settings.urls')),
    path('administration/', include('administration.urls')),
    path('healthy/<int:id>/', healthy, name='healthy'),
    path('alert/', webhook, name='alert'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('clients/', include('clients.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('projects/<int:application_id>/notifications/', include('notifications.urls')),
    url(r'^logout/$', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]
