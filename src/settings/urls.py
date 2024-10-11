from django.urls import path

from .views import settings, user_delete, user_timezone_form

urlpatterns = [
    path('', settings, name='settings'),
    path('user/timezone', user_timezone_form, name='user_timezone_form'),
    path('user/delete', user_delete, name='user_delete'),
]
