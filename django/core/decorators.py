from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render
 
def user_approved_in_waiting_list(user):
    if user.is_staff:
        return True
    return False

def waiting_list_approved_only():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            if not user_approved_in_waiting_list(request.user):
                return render(request, 'waiting_list.html')
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator