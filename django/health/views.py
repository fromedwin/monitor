import os
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from projects.models import HTTPMockedCodeService

# Create your views here.
def healthy(request, id):

    obj = get_object_or_404(HTTPMockedCodeService, pk=id)

    return HttpResponse(status=obj.code, content=obj.code)