from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.loader import render_to_string
from fromedwin.decorators import waiting_list_approved_only
from .models import CeleryTaskLog

@login_required
@waiting_list_approved_only()
def logs(request):
    """
    Display logs page - Shows CeleryTaskLog entries for user's projects
    Supports infinite scroll pagination via AJAX
    """
    # Get all logs for projects that belong to the current user
    user_logs = CeleryTaskLog.objects.filter(
        project__in=request.user.projects.all()
    ).select_related('project', 'project__favicon_details').prefetch_related('lighthouse__page')
    
    # Filter by task name if provided
    task_name_filter = request.GET.get('task_name', '').strip()
    if task_name_filter:
        user_logs = user_logs.filter(task_name__icontains=task_name_filter)
    
    # Filter by project if provided
    project_filter = request.GET.get('project', '').strip()
    if project_filter:
        user_logs = user_logs.filter(project_id=project_filter)
    
    user_logs = user_logs.order_by('-created_at')
    
    # Pagination
    page_size = 100  # Number of logs per page
    page = request.GET.get('page', 1)
    paginator = Paginator(user_logs, page_size)
    logs_page = paginator.get_page(page)
    
    # If this is an AJAX request, return JSON data
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        log_items_html = render_to_string('logs/log_items.html', {
            'logs': logs_page,
        }, request=request)
        
        return JsonResponse({
            'html': log_items_html,
            'has_next': logs_page.has_next(),
            'next_page_number': logs_page.next_page_number() if logs_page.has_next() else None,
        })
    
    # For initial page load, get additional data for filters
    unique_task_names = CeleryTaskLog.objects.filter(
        project__in=request.user.projects.all()
    ).values_list('task_name', flat=True).distinct().order_by('task_name')
    
    user_projects = request.user.projects.all().order_by('title')
    
    return render(request, 'logs/logs.html', {
        'logs': logs_page,
        'logs_count': user_logs.count(),
        'task_name_filter': task_name_filter,
        'project_filter': project_filter,
        'unique_task_names': unique_task_names,
        'user_projects': user_projects,
        'has_next': logs_page.has_next(),
        'next_page_number': logs_page.next_page_number() if logs_page.has_next() else None,
    })
