from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def logs(request):
    """
    Display logs page - Coming soon
    """
    return render(request, 'logs/logs.html')
