from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class TestApi(APITestCase):

    def test_get_list_without_signin(self):
        response = self.client.get('/list/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_with_signin(self):
        user = User.objects.create_user(username='Admin', password='qwe')
        self.client.force_authenticate(user=user)
        response = self.client.get('/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_save_list_without_signin(self):
        data = {'name': '', 'owner': 1}
        response = self.client.post('/list/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_save_list_with_empty_name(self):
        user = user = User.objects.create_user(
            username='Admin', password='qwe')
        self.client.force_authenticate(user=user)
        data = {'name': '', 'owner': user.id}
        response = self.client.post('/list/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
