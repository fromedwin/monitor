import logging
import json
from datetime import timedelta
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from projects.models import Project
from .models import ProjectReport
from logs.models import CeleryTaskLog
from .tasks.create_report import create_report


@api_view(['POST'])
def queue_report_generation(request, project_id):
    """
    Queue a report generation task for a specific project.
    """
    try:
        # Get the project
        project = get_object_or_404(Project, id=project_id)
        
        # Queue the report creation task
        task = create_report.delay(project_id, project.url)
        
        return JsonResponse({
            'success': True,
            'message': f'Report generation queued for {project.title}',
            'task_id': task.id,
            'project_id': project_id
        })
        
    except Project.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Project not found'
        }, status=404)
    except Exception as e:
        logging.error(f"Error queuing report generation for project {project_id}: {e}")
        return JsonResponse({
            'success': False,
            'error': 'An error occurred while queuing the report generation'
        }, status=500)

