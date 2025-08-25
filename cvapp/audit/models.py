from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class RequestLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    http_method = models.CharField(max_length=16)
    path = models.CharField(max_length=255)
    query_string = models.TextField(blank=True)
    remote_ip = models.GenericIPAddressField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.http_method} {self.path} at {self.timestamp}"
