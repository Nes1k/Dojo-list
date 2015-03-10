from django.db import models
from django.conf import settings


class List(models.Model):
    name = models.CharField(max_length=60)

    class Meta:
        verbose_name = "Lista"
        verbose_name_plural = "Listy"

    def __str__(self):
        return self.name


class Action(models.Model):
    text = models.CharField(max_length=60)
    done = models.BooleanField(default=False)
    list = models.ForeignKey(List)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Action"
        verbose_name_plural = "Actions"
        unique_together = ('list', 'text')
