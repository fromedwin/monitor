from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.conf import settings
from django.urls import reverse
from django.shortcuts import redirect

from fromedwin.decorators import waiting_list_approved_only
from .forms import TimeZoneForm

@login_required
@waiting_list_approved_only()
def profile(request):
    """
    Set user profile
    """
    profile = request.user.profile

    if request.POST and 'disable_auto_redirect' in request.POST:
        profile.disable_auto_redirect = not profile.disable_auto_redirect
        profile.save()
        return redirect(reverse('profile'))

    return render(request, 'profile.html', { 
        'settings': settings, 
        'profile': profile,
    })

@login_required
@waiting_list_approved_only()
def user_timezone_form(request):
    """
        Create or edit service model
    """
    # Sort timeones by string value

    profile = request.user.profile if hasattr(request.user, 'profile') else None

    if request.POST:
        form = TimeZoneForm(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()
            return redirect(reverse('profile'))

        return render(request, 'user/timezone.html', {'form': form})

    form = TimeZoneForm(instance=profile)

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
        request.user.delete()
        logout(request)
        return render(request, 'user/delete_done.html', {})

    return render(request, 'user/delete_confirmation.html', {})
