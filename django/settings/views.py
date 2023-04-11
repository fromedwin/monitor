from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings as django_settings

@login_required
def settings(request):
    """
    Set user settings
    """
    return render(request, 'settings.html', { 'settings': django_settings })


@login_required
def user_delete(request):
    """
        Create or edit service model
    """
    if request.POST:
        #request.user.delete()
        logout(request)
        return render(request, 'user/delete_done.html', {})

    return render(request, 'user/delete_confirmation.html', {})
