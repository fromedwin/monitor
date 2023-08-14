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
from django.conf import settings
from django.urls import path, include

from .views import restricted, healthcheck_database, healthcheck_workers_availability, healthcheck_workers_lighthouse
from alerts.api import webhook
from website.views import homepage
from dashboard.views import dashboard

from django.conf.urls.static import static

from allauth.account.views import login

urlpatterns = [
    # """
    # Project URLs
    # """
    path('', include('projects.urls')),
    path('', include('availability.urls')),
    path('', include('notifications.urls')),
    path('', include('performances.urls')),
    path('', include('status.urls')),
    path('', include('website.urls')),
    path('', include('alerts.urls')),
    # monitor-worker api
    path('clients/', include('workers.urls')),
    # Settings URL
    path('settings/', include('settings.urls')),
    # User dahsboard with feed
    path('dashboard/', dashboard, name='dashboard'),
    # Login page from allauth with github button
    path('login/', login, name='login'),
    # Webhook to receive alerts
    path('alert/', webhook, name='alert'),
    # Display restricted message for user trying to login
    path('restricted/', restricted, name='restricted'),
    # Administration panel for super user in app
    path('administration/', include('administration.urls')),

    # """
    # Healthcheck APIs
    # """
    path('healthcheck/database/', healthcheck_database, name='healthcheck_database'),
    path('healthcheck/availability/', healthcheck_workers_availability, name='healthcheck_availability'),
    path('healthcheck/lighthouse/', healthcheck_workers_lighthouse, name='healthcheck_lighthouse'),

    # """
    # Dependencies URLs
    # """

    # Django admin
    path('admin/', admin.site.urls),
    # Django allauth accounts
    path('accounts/', include('allauth.urls')),
    # Autentication API for rest_framework
    path('api-auth/', include('rest_framework.urls')),
    # Logout view
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    # Django prometheus, adding /metrics url
    path('', include('django_prometheus.urls')),
    # Tailwind reload event
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
