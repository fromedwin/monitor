from django.urls import path

from .views import settings, user_delete

urlpatterns = [
    path('', settings, name='settings'),
    path('user/delete', user_delete, name='user_delete'),
]
