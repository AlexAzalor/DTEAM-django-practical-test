from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CV, Skill, Project

CV_TEST_DATA = {
    "firstname": "John",
    "lastname": "Doe",
    "role": "Full Stack Developer",
    "bio": "Experienced developer with 5 years of experience",
    "contacts": "john.doe@example.com"
}
TEST_DJANGO = "Django"
TEST_REACT = "React"

class MainViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test CVs
        self.cv1 = CV.objects.create(**CV_TEST_DATA)

    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CVDetailsViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test CV
        self.cv = CV.objects.create(**CV_TEST_DATA)

    def test_cv_details(self):
        response = self.client.get(f'/cv_page/{self.cv.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'cv_page.html')
        self.assertEqual(response.context['cv_item'], self.cv)

    def test_cv_details_invalid_pk(self):
        non_existent_id = 535435
        response = self.client.get(f'/cv_page/{non_existent_id}/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cv_details_content(self):
        response = self.client.get(f'/cv_page/{self.cv.id}/')
        cv_item = response.context['cv_item']

        self.assertEqual(cv_item.firstname, CV_TEST_DATA["firstname"])
        self.assertEqual(cv_item.lastname, CV_TEST_DATA["lastname"])
        self.assertEqual(cv_item.role, CV_TEST_DATA["role"])
        self.assertEqual(cv_item.bio, CV_TEST_DATA["bio"])
        self.assertEqual(cv_item.contacts, CV_TEST_DATA["contacts"])


class CVAPITests(APITestCase):
    def setUp(self):
        # Create test skills
        self.skill1 = Skill.objects.create(name=TEST_DJANGO)
        self.skill2 = Skill.objects.create(name=TEST_REACT)

        # Create test projects
        self.project1 = Project.objects.create(
            title="E-commerce App",
            description="A full-stack e-commerce application",
            link="https://example.com"
        )
        self.project2 = Project.objects.create(
            title="Blog Platform",
            description="A content management system for blogs",
            link="https://example2.com"
        )

        # Create test CV
        self.cv = CV.objects.create(**CV_TEST_DATA)
        self.cv.skills.set([self.skill1, self.skill2])
        self.cv.projects.set([self.project1])

    def test_cv_get_list(self):
        url = reverse('cv-list-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(len(data), 1)

        cv_data = data[0]
        self.assertEqual(cv_data['firstname'], self.cv.firstname)
        self.assertEqual(cv_data['lastname'], self.cv.lastname)

        self.assertEqual(len(cv_data['skills']), 2)
        self.assertEqual(len(cv_data['projects']), 1)

    def test_cv_create(self):
        url = reverse('cv-list-create')
        new_cv_data = {
            **CV_TEST_DATA,
            "skill_ids": [self.skill2.id],
            "project_ids": [self.project2.id]
        }

        response = self.client.post(url, new_cv_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()

        self.assertEqual(data['firstname'], CV_TEST_DATA["firstname"])
        self.assertEqual(data['lastname'], CV_TEST_DATA["lastname"])

        self.assertEqual(len(data['skills']), 1)
        self.assertEqual(len(data['projects']), 1)

        self.assertEqual(CV.objects.count(), 2)

    def test_cv_get_by_id(self):
        url = reverse('cv-detail', args=[self.cv.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data['id'], self.cv.id)

    def test_cv_partial_update_patch_name_only(self):
        url = reverse('cv-detail', args=[self.cv.id])

        # Update only the firstname
        new_name = "Janet"
        patch_data = {
            "firstname": new_name
        }

        response = self.client.patch(url, patch_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()

        self.assertEqual(data['firstname'], new_name)
        self.assertEqual(data['lastname'], self.cv.lastname)


    def test_cv_delete(self):
        url = reverse('cv-detail', args=[self.cv.id])

        self.assertEqual(CV.objects.count(), 1)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CV.objects.count(), 0)

    def test_cv_create_missing_required_fields(self):
        url = reverse('cv-list-create')
        incomplete_data = {
            "firstname": "Test"
        }

        response = self.client.post(url, incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
