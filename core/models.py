from django.db import models
from django.conf import settings


class Action(models.Model):
    text = models.CharField(max_length=60)
    done = models.BooleanField(default=False)
    list = models.ForeignKey('List')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Action"
        verbose_name_plural = "Actions"
        unique_together = ('list', 'text')


class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=60)

    class Meta:
        verbose_name = "Lista"
        verbose_name_plural = "Listy"
        unique_together = ('owner', 'name')

    def __str__(self):
        return self.name

    @property
    def todo(self):
        actions = Action.objects.filter(list=self.id)
        total = 0
        for item in actions:
            if not item.done:
                total += 1
        return total
