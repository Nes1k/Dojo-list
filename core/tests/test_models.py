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

    def test_cannot_save_list_without_name(self):
        list_ = List()
        with self.assertRaises(ValidationError):
            list_.save()
            list_.full_clean()

    def test_cannot_save_empty_list_actions(self):
        list_ = List.objects.create(name='Sklep')
        action = Action(text='', list=list_)
        with self.assertRaises(ValidationError):
            action.save()
            action.full_clean()
