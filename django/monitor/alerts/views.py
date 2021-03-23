from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Alert
# Create your views here.

@api_view(['POST'])
def webhook(request):
    print(request.data)

    alert = Alert(json=request.data)
    alert.save()

    return Response()
