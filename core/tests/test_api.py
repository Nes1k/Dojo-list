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
        data = {'name': ''}
        response = self.client.post('/list/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_save_list_with_empty_name(self):
        user = user = User.objects.create_user(
            username='Admin', password='qwe')
        self.client.force_authenticate(user=user)
        data = {'name': ''}
        response = self.client.post('/list/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_see_only_own_list(self):
        user1 = User.objects.create_user(username='user1', password='qwe')
        user2 = User.objects.create_user(username='user2', password='qwe')
        data = {'name': 'Zakupy'}
        self.client.force_authenticate(user=user1)
        self.client.post('/list/', data, format='json')
        self.client.logout()
        self.client.force_authenticate(user=user2)
        data = {'name': 'Bla'}
        self.client.post('/list/', data, format='json')
        response = self.client.get('/list/')
        self.assertNotIn(b'Zakupy', response.content)
        self.assertEqual(
            response.content, b'[{"id":2,"name":"Bla"}]')
