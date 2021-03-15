import os
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def healthy(request):
    print(os.environ['HEALTHY'])
    try:
        if os.environ['HEALTHY'] == '500':
            return HttpResponse(status=500, content='500')
        if os.environ['HEALTHY'] == '404':
            return HttpResponse(status=404, content='404')
        if os.environ['HEALTHY'] == '400':
            return HttpResponse(status=400, content='400')
        if os.environ['HEALTHY'] == '200':
            return HttpResponse(status=200, content='200')
        return HttpResponse("OK")
    except:
        return HttpResponse("OK")