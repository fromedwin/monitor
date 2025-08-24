import logging
import json
from datetime import timedelta
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from projects.models import Project
from .models import ProjectReport
from logs.models import CeleryTaskLog
from .tasks.create_report import create_report


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def queue_report_generation(request, project_id):
    """
    Queue a report generation task for a specific project.
    """
    try:
        # Get the project
        project = get_object_or_404(Project, id=project_id)
        
        # Verify user owns the project
        if project.user != request.user:
            return JsonResponse({
                'success': False,
                'error': 'Access denied. You do not own this project.'
            }, status=403)
        
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_report_by_id(request, report_id):
    """
    Fetch a specific report by ID.
    Ensures the user owns the project associated with the report.
    """
    try:
        # Get the report
        report = get_object_or_404(ProjectReport, id=report_id)
        
        # Verify user owns the project
        if report.project.user != request.user:
            return JsonResponse({
                'success': False,
                'error': 'Access denied. You do not own this report.'
            }, status=403)
        
        return JsonResponse({
            'success': True,
            'report': {
                'id': report.id,
                'project_id': report.project.id,
                'project_title': report.project.title,
                'data': report.data,
                'creation_date': report.creation_date.isoformat(),
                'celery_task_log_id': report.celery_task_log.id if report.celery_task_log else None
            }
        })
        
    except ProjectReport.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Report not found'
        }, status=404)
    except Exception as e:
        logging.error(f"Error fetching report {report_id}: {e}")
        return JsonResponse({
            'success': False,
            'error': 'An error occurred while fetching the report'
        }, status=500)

