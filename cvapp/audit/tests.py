from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from unittest.mock import Mock
from .middleware import RequestLoggingMiddleware
from .models import RequestLog

User = get_user_model()

TEST_USER = {
    'username': 'johnsmith',
    'email': 'test@example.com',
    'password':'12345'
}


class RequestLoggingMiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username=TEST_USER['username'],
            email=TEST_USER['email'],
            password='testpass123'
        )

        self.mock_get_response = Mock(return_value=HttpResponse('OK'))
        self.middleware = RequestLoggingMiddleware(self.mock_get_response)

    def test_middleware_logs_get(self):
        request = self.factory.get('/api/cvs/')
        request.user = self.user

        self.assertEqual(RequestLog.objects.count(), 0)

        response = self.middleware(request)

        self.assertEqual(response.status_code, 200)
        self.mock_get_response.assert_called_once_with(request)

        self.assertEqual(RequestLog.objects.count(), 1)

        log = RequestLog.objects.first()
        self.assertEqual(log.http_method, 'GET')
        self.assertEqual(log.path, '/api/cvs/')
        self.assertEqual(log.query_string, '')
        self.assertEqual(log.user, self.user)
        self.assertIsNotNone(log.timestamp)

    def test_middleware_logs_post(self):
        request = self.factory.post('/api/cvs/', data={'name': 'test'})
        request.user = self.user

        self.middleware(request)
        self.assertEqual(RequestLog.objects.count(), 1)

        log = RequestLog.objects.first()
        self.assertEqual(log.http_method, 'POST')
        self.assertEqual(log.path, '/api/cvs/')
        self.assertEqual(log.user, self.user)

    def test_middleware_logs_with_query_string(self):
        request = self.factory.get('/api/cvs/?search=python&page=2')
        request.user = self.user

        self.middleware(request)

        log = RequestLog.objects.first()
        self.assertEqual(log.path, '/api/cvs/')
        self.assertEqual(log.query_string, 'search=python&page=2')

    def test_middleware_handles_different_http_methods(self):
        methods_and_factories = [
            ('GET', self.factory.get),
            ('POST', self.factory.post),
            ('PUT', self.factory.put),
            ('PATCH', self.factory.patch),
            ('DELETE', self.factory.delete),
        ]

        for method_name, factory_method in methods_and_factories:
            with self.subTest(method=method_name):
                # Clear existing logs
                RequestLog.objects.all().delete()

                request = factory_method('/api/test/')
                request.user = self.user

                self.middleware(request)

                self.assertEqual(RequestLog.objects.count(), 1)
                log = RequestLog.objects.first()
                self.assertEqual(log.http_method, method_name)
                self.assertEqual(log.path, '/api/test/')
