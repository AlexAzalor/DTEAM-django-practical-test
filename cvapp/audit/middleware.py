from .models import RequestLog
from django.utils.timezone import now

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        # Avoid logging admin/static
        if request.path.startswith('/admin') or request.path.startswith('/static') or request.path.startswith('/favicon.ico'):
            return response

        http_method = request.method
        path = request.path
        query_string = request.META.get('QUERY_STRING', '')
        remote_ip = self.get_client_ip(request)
        user = request.user if request.user.is_authenticated else None

        try:
            RequestLog.objects.create(
                http_method=http_method,
                path=path[:255], # Truncate path to fit model field
                query_string=query_string,
                remote_ip=remote_ip,
                user=user
            )
        except Exception:
            # Silently handle database errors to not break request processing
            pass

        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
