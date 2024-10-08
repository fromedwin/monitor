from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail

from allauth.socialaccount.models import SocialApp

from workers.models import Server

from django.db.models import Q
from performances.models import Performance
from availability.models import Service
from constants import LIGHTHOUSE_FORMFACTOR_CHOICES

@staff_member_required
def administration(request):
    """
    Show administration data
    """
    token = None
    is_staff = False
    servers = []

    # if get success exist boolean true
    email_success = False
    email_fail = False
    
    if 'email_success' in request.GET:
        email_success = True
    
    if 'email_fail' in request.GET:
        email_success = True

    servers = Server.objects.filter(
        last_seen__gte=timezone.now() - timezone.timedelta(seconds=settings.HEARTBEAT_INTERVAL+5)
    ).order_by('-creation_date')

    inQueueLighthouse = Performance.objects.filter(Q(request_run=True) | Q(last_request_date__isnull=True) | Q(last_request_date__lt=timezone.now()-timezone.timedelta(minutes=settings.LIGHTHOUSE_SCRAPE_INTERVAL_MINUTES))).count()
    totalLighthouse = Performance.objects.count()

    return render(request, 'administration.html', {
        'servers': servers,
        'settings': settings,
        'email_success': email_success,
        'email_fail': email_fail,
        'stats': {
            'inQueueLighthouse': inQueueLighthouse / totalLighthouse * 100,
            'users_count': User.objects.count,
            'url_count': Service.objects.count,
            'performance_count': inQueueLighthouse / Performance.objects.count() * 100,
        }
    })


@staff_member_required
def test_email(request):

    success = True
    # Send test email
    try:
        send_mail(
            'Test email',
            'This is a test email',
            f"{settings.CONTACT_NAME} <{settings.CONTACT_EMAIL}>",
            [request.user.email],
            fail_silently=False,
        )
    except Exception as e:
        print(e)
        success = False

    return redirect(f"{reverse('administration')}{ '?email_success' if success else 'email_fail' }")
