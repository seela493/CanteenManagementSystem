from django.shortcuts import render

def start_view(request):
    return render(request, 'Start/start.html')