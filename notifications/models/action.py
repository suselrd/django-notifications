# coding=utf-8

from django.db import models


class Action(models.Model):
    name = models.CharField(max_length=50, unique=True)
    read_as = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        app_label = 'notifications'

    def __unicode__(self):
        return self.read_as
