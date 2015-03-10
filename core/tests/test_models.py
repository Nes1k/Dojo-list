# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.exceptions import ValidationError
from core.models import List, Action


class ListAndActionModelsTest(TestCase):

    def test_item_is_related_to_list(self):
        list_ = List.objects.create(name='Zakupy')
        action = Action(text='Pomidory')
        action.list = list_
        action.save()

        self.assertIn(action, list_.action_set.all())

    def test_cannot_save_empty_list_actions(self):
        list_ = List.objects.create(name='Sklep')
        action = Action(text='', list=list_)
        with self.assertRaises(ValidationError):
            action.save()
            action.full_clean()

    def test_duplicate_actions_are_invalid(self):
        list_ = List.objects.create(name='Zakupy')
        Action.objects.create(text='Pomidory', list=list_)
        with self.assertRaises(ValidationError):
            action = Action(text='Pomidory', list=list_)
            action.full_clean()

    def test_can_save_same_action_to_different_lists(self):
        list1 = List.objects.create(name='Zakupy')
        list2 = List.objects.create(name='Wydatki')
        Action.objects.create(text='Pomidory', list=list1)
        action = Action.objects.create(text='Pomidory', list=list2)
        action.full_clean()


class ListModelTest(TestCase):

    def test_cannot_save_list_without_name(self):
        list_ = List()
        with self.assertRaises(ValidationError):
            list_.save()
            list_.full_clean()
