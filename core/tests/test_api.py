from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from core.models import List, Action


class ListMixin(APITestCase):

    def makeList(self, name='', username='user'):
        user = User.objects.create_user(username=username, password='qwe')
        self.client.force_authenticate(user=user)
        data = {'name': name}
        return self.client.post('/list/', data, format='json')


class TestListAPI(ListMixin):

    def test_get_list_without_signin(self):
        response = self.client.get('/list/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_with_signin(self):
        user = User.objects.create_user(username='user', password='qwe')
        self.client.force_authenticate(user=user)
        response = self.client.get('/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cannot_save_list_without_signin(self):
        data = {'name': ''}
        response = self.client.post('/list/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(List.objects.all().count(), 0)

    def test_cannot_save_list_with_empty_name(self):
        response = self.makeList()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(List.objects.all().count(), 0)

    def test_duplicate_list_are_invalid(self):
        self.makeList('Zakupy')
        response = self.client.post(
            '/list/', {'name': 'Zakupy'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_see_only_own_list(self):
        self.makeList(name='Zakupy', username='user1')
        self.client.logout()
        self.makeList(name='Bla', username='user2')
        response = self.client.get('/list/')
        self.assertNotIn(b'Zakupy', response.content)
        self.assertEqual(response.content, b'[{"id":2,"name":"Bla","todo":0}]')

    def test_put_list(self):
        self.makeList('Zakupy')
        data = {'name': 'Projekt'}
        response = self.client.put('/list/1/', data, format='json')
        self.assertEqual(
            response.content, b'{"id":1,"name":"Projekt","todo":0}')
        self.assertEqual(List.objects.all().count(), 1)

    def test_delete_list(self):
        self.makeList('Zakupy')
        response = self.client.delete('/list/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get('/list/')
        self.assertEqual(response.content, b'[]')
        self.assertEqual(List.objects.all().count(), 0)


class TestAction(ListMixin):

    def test_cannot_save_action_with_empty_text(self):
        self.makeList(name='Zakupy')
        data = {'text': ''}
        response = self.client.post('/list/1/actions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Action.objects.all().count(), 0)

    def test_can_save_action(self):
        self.makeList(name='Zakupy')
        data = {'text': 'Pomidory'}
        response = self.client.post('/list/1/actions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Action.objects.all().count(), 1)

    def test_POST_duplicate_list_are_invalid(self):
        self.makeList(name='Zakupy')
        data = {'text': 'Pomidory'}
        self.client.post('/list/1/actions/', data, format='json')
        response = self.client.post('/list/1/actions/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_PUT_duplicate_list_are_invalid(self):
        self.makeList(name='Zakupy')
        data = {'text': 'Pomidory'}
        self.client.post('/list/1/actions/', data, format='json')
        self.client.post('/list/1/actions/', {'text': 'Zakupy'}, format='json')
        response = self.client.put('/list/1/actions/2/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_see_only_own_action(self):
        self.makeList(name='Zakupy')
        data = {'text': 'Pomidory'}
        self.client.post('/list/1/actions/', data, format='json')
        self.client.logout()
        user1 = User.objects.create_user(username='user1', password='qwe')
        self.client.force_authenticate(user=user1)
        response = self.client.get('/list/1/actions/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_action(self):
        self.makeList(name='Zakupy')
        data1 = {'text': 'Pomidory'}
        self.client.post('/list/1/actions/', data1, format='json')
        data2 = {'text': 'Cytryna'}
        response = self.client.put('/list/1/actions/1/', data2, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(b'"text":"Cytryna"', response.content)
        self.assertEqual(Action.objects.all().count(), 1)

    def test_delete_action(self):
        self.makeList(name='Zakupy')
        data1 = {'text': 'Pomidory'}
        self.client.post('/list/1/actions/', data1, format='json')
        response = self.client.delete('/list/1/actions/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Action.objects.all().count(), 0)
