from django.shortcuts import render

def restricted(request):
    return render(request, 'restricted.html')
