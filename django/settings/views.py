from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings as django_settings
from django.urls import reverse
from django.shortcuts import redirect

from .forms import TimeZoneForm

@login_required
def settings(request):
    """
    Set user settings
    """

    profile = request.user.profile

    return render(request, 'settings.html', { 
        'settings': django_settings, 
        'profile': profile,
    })

@login_required
def user_timezone_form(request):
    """
        Create or edit service model
    """
    # Sort timeones by string value

    profile = request.user.profile if hasattr(request.user, 'profile') else None

    if request.POST:
        form = TimeZoneForm(request.POST, instance=request.user.profile)
        form.fields['timezone'].choices.sort(key=lambda x: x[1])

        if form.is_valid():
            form.save()
            return redirect(reverse('settings'))

        return render(request, 'user/timezone.html', {'form': form})

    form = TimeZoneForm(instance=profile)
    form.fields['timezone'].choices.sort(key=lambda x: x[1])

    return render(request, 'user/timezone.html', {
        'form': form,
        'profile': profile
    })

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
