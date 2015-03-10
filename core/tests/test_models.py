# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from core.models import List, Action


class ListAndActionModelsTest(TestCase):

    def test_item_is_related_to_list(self):
        user = User.objects.create_user(username='user', password='qwe')
        list_ = List.objects.create(owner=user, name='Zakupy')
        action = Action(text='Pomidory')
        action.list = list_
        action.save()

        self.assertIn(action, list_.action_set.all())

    def test_cannot_save_empty_list_actions(self):
        user = User.objects.create_user(username='user', password='qwe')
        list_ = List.objects.create(owner=user, name='Sklep')
        action = Action(text='', list=list_)
        with self.assertRaises(ValidationError):
            action.save()
            action.full_clean()

    def test_duplicate_actions_are_invalid(self):
        user = User.objects.create_user(username='user', password='qwe')
        list_ = List.objects.create(owner=user, name='Zakupy')
        Action.objects.create(text='Pomidory', list=list_)
        with self.assertRaises(ValidationError):
            action = Action(text='Pomidory', list=list_)
            action.full_clean()

    def test_can_save_same_action_to_different_lists(self):
        user = User.objects.create_user(username='user', password='qwe')
        list1 = List.objects.create(owner=user, name='Zakupy')
        list2 = List.objects.create(owner=user, name='Projekty')
        Action.objects.create(text='Pomidory', list=list1)
        action = Action.objects.create(text='Pomidory', list=list2)
        action.full_clean()


class ListModelTest(TestCase):

    def test_cannot_save_list_without_name(self):
        user = User.objects.create_user(username='user', password='qwe')
        list_ = List(owner=user)
        with self.assertRaises(ValidationError):
            list_.save()
            list_.full_clean()

    def test_duplicate_list_are_invalid(self):
        user = User.objects.create_user(username='user', password='qwe')
        List.objects.create(owner=user, name='Zakupy')
        with self.assertRaises(ValidationError):
            list = List(owner=user, name='Zakupy')
            list.full_clean()

    def test_can_save_same_list_to_different_user(self):
        user1 = User.objects.create_user(username='user1', password='qwe')
        user2 = User.objects.create_user(username='user2', password='qwe')
        List.objects.create(owner=user1, name='Zakupy')
        list = List(owner=user2, name='Zakupy')
        list.full_clean()
