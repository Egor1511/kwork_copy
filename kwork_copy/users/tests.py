from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, URLPatternsTestCase, APIClient

from users.models import FreelancerProfile
from users.urls import urlpatterns


class Tests(APITestCase, URLPatternsTestCase):
    urlpatterns += urlpatterns
    User = get_user_model()

    def test_register_user(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        url = reverse('register')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(self.User.objects.filter(username='testuser').exists())
        self.assertTrue(FreelancerProfile.objects.filter(
            user__username='testuser').exists())

    def test_register_invalid_data(self):
        data = {
            'username': 'testuser',
            'email': 'invalidemail',
            'password': 'testpassword',
        }
        url = reverse('register')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(self.User.objects.filter(username='testuser').exists())

class ProfileViewTestCase(APITestCase, URLPatternsTestCase):
    urlpatterns += urlpatterns
    User = get_user_model()
    def setUp(self):
        self.client = APIClient()
        self.user = self.User.objects.create(username='testuser', email='test@example.com')
        self.profile = FreelancerProfile.objects.create(user=self.user)

    def test_get_profile(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_profile_not_authenticated(self):
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_profile(self):
        self.client.force_authenticate(user=self.user)
        data = {'contact_info': 'updated_value'}
        url = reverse('profile')
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.profile.contact_info, 'updated_value')