from django.shortcuts import render
from .models import RequestLog

def recent_logs(request):
    # Get the 10 most recent logs
    logs = RequestLog.objects.all().order_by('-timestamp')[:10]
    return render(request, 'audit/recent_logs.html', {'logs': logs})
