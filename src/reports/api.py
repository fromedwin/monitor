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

