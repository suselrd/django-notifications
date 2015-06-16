# coding=utf-8

from django.db import models


class ActionManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class Action(models.Model):
    name = models.CharField(max_length=50, unique=True)
    read_as = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, default='')

    objects = ActionManager()

    class Meta:
        app_label = 'notifications'

    def __unicode__(self):
        return self.read_as

    def natural_key(self):
        return self.name,
