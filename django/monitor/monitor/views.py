from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404

from projects.models import Project
from incidents.models import InstanceDownIncident

def public(request, id):
    """
    Show Public view of a project status
    """

    project = get_object_or_404(Project, pk=id)

    if not project.enable_public_page:
        raise Http404()

    number_days = 30

    start_date = timezone.now() - timezone.timedelta(days=number_days)
    incidents = InstanceDownIncident.objects.filter(service__project=project, startsAt__gte=start_date, severity=2)

    days = []
    for day in range(number_days):
        day = timezone.now() - timezone.timedelta(days=day)
        start_of_day = timezone.datetime(day.year,day.month,day.day)
        end_of_day = start_of_day + timezone.timedelta(days=1)

        days.append({
            'day': start_of_day,
            'incidents': InstanceDownIncident.objects.filter(service__project=project, severity=2).filter(Q(startsAt__gte=start_of_day, endsAt__lt=end_of_day)|Q(startsAt__lt=start_of_day, endsAt__gt=start_of_day)|Q(startsAt__lt=end_of_day, endsAt__gt=end_of_day)).order_by('startsAt'),
            'outrage': InstanceDownIncident.objects.filter(service__project=project, severity=2, service__is_critical=True).filter(Q(startsAt__gte=start_of_day, endsAt__lt=end_of_day)|Q(startsAt__lt=start_of_day, endsAt__gt=start_of_day)|Q(startsAt__lt=end_of_day, endsAt__gt=end_of_day)),
            'degradated': InstanceDownIncident.objects.filter(service__project=project, severity=2, service__is_critical=False).filter(Q(startsAt__gte=start_of_day, endsAt__lt=end_of_day)|Q(startsAt__lt=start_of_day, endsAt__gt=start_of_day)|Q(startsAt__lt=end_of_day, endsAt__gt=end_of_day)),
        })

    return render(request, 'public.html', {
        'project': project,
        'incidents': incidents,
        'days': days
    })