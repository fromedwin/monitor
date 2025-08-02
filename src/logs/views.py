from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from fromedwin.decorators import waiting_list_approved_only
from .models import CeleryTaskLog

@login_required
@waiting_list_approved_only()
def logs(request):
    """
    Display logs page - Shows CeleryTaskLog entries for user's projects
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
    
    # Get unique task names for the filter dropdown
    unique_task_names = CeleryTaskLog.objects.filter(
        project__in=request.user.projects.all()
    ).values_list('task_name', flat=True).distinct().order_by('task_name')
    
    # Get user's projects for the project filter dropdown
    user_projects = request.user.projects.all().order_by('title')
    
    user_logs = user_logs.order_by('-created_at')
    
    return render(request, 'logs/logs.html', {
        'logs': user_logs,
        'logs_count': user_logs.count(),
        'task_name_filter': task_name_filter,
        'project_filter': project_filter,
        'unique_task_names': unique_task_names,
        'user_projects': user_projects,
    })
