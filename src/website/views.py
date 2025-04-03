from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse

from allauth.socialaccount.models import SocialApp

from core.decorators import saas_only

@saas_only()
def homepage(request):
    """
    Home Welcome page
    """

    if request.user and request.user.is_authenticated:
        if not request.user.profile.disable_auto_redirect:
            return redirect(reverse('dashboard'))

    socialapps = SocialApp.objects.all()

    return render(request, 'homepage.html', {
        'socialapps': socialapps,
        'is_authenticated': request.user.is_authenticated
    })

@saas_only()
def pricing(request):
    return render(request, 'pricing.html', {
        'is_authenticated': request.user.is_authenticated,
        'settings': settings,
    })

@saas_only()
def features(request):
    return render(request, 'features.html', {
        'is_authenticated': request.user.is_authenticated
    })

@saas_only()
def legal(request):
    return render(request, 'legal.html', {
        'is_authenticated': request.user.is_authenticated
    })

@saas_only()
def aboutus(request):
    return render(request, 'about-us.html', {
        'is_authenticated': request.user.is_authenticated
    })
