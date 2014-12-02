# coding=utf-8
from django.db import models


class Transport(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    cls = models.CharField(max_length=255, null=False)
    allows_freq_config = models.BooleanField(default=False)
    allows_context = models.BooleanField(default=False)
    delete_sent = models.BooleanField(default=True)
    allows_subscription = models.BooleanField(default=True)

    class Meta:
        app_label = "notifications"

    def __unicode__(self):
        return self.name or self.cls
