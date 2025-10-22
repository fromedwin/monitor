from functools import wraps
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
 
def user_approved_in_waiting_list(user):
    """
    Check if a user is approved in the waiting list.
    """
    if user.is_staff:
        return True
    return False

def waiting_list_approved_only():
    """
    Decorator to check if a user is approved in the waiting list.
    """
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if settings.SAAS and not user_approved_in_waiting_list(request.user):
                return render(request, 'waiting_list.html')
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def saas_only():
    """
    If settings.SAAS is False, redirect to login page. Otherwise render view as expected.
    """
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not settings.SAAS:
                return redirect(reverse('login'))
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator