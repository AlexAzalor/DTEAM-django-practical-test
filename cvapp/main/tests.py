from django.test import TestCase, Client
from django.urls import reverse
from django.http import Http404
from .models import CV, Skill, Project

# Create your tests here.

CV_TEST_DATA = {
    "firstname": "John",
    "lastname": "Doe",
    "role": "Full Stack Developer",
    "bio": "Experienced developer with 5 years of experience",
    "contacts": "john.doe@example.com"
}

class MainViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test CVs
        self.cv1 = CV.objects.create(**CV_TEST_DATA)

    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_main_page_uses_correct_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'index.html')

    def test_main_page_contains_all_cvs(self):
        response = self.client.get('/')
        cv_items = response.context['cv_items']

        # Check that all CVs are in the context
        self.assertEqual(len(cv_items), 1)
        self.assertIn(self.cv1, cv_items)

    def test_main_page_empty_cv_list(self):
        CV.objects.all().delete()

        response = self.client.get('/')
        cv_items = response.context['cv_items']

        # Should return empty queryset
        self.assertEqual(len(cv_items), 0)
        self.assertEqual(response.status_code, 200)


class CVDetailsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test CV
        self.cv = CV.objects.create(**CV_TEST_DATA)

    def test_cv_details(self):
        response = self.client.get(f'/cv_page/{self.cv.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cv_page.html')
        self.assertEqual(response.context['cv_item'], self.cv)

    def test_cv_details_invalid_pk(self):
        non_existent_id = 535435
        response = self.client.get(f'/cv_page/{non_existent_id}/')

        self.assertEqual(response.status_code, 404)

    def test_cv_details_content(self):
        response = self.client.get(f'/cv_page/{self.cv.id}/')
        cv_item = response.context['cv_item']

        self.assertEqual(cv_item.firstname, CV_TEST_DATA["firstname"])
        self.assertEqual(cv_item.lastname, CV_TEST_DATA["lastname"])
        self.assertEqual(cv_item.role, CV_TEST_DATA["role"])
        self.assertEqual(cv_item.bio, CV_TEST_DATA["bio"])
        self.assertEqual(cv_item.contacts, CV_TEST_DATA["contacts"])
