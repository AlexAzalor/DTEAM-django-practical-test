from django.urls import path
from .views import recent_logs

urlpatterns = [
    path('logs/', recent_logs, name='recent-logs'),
]
