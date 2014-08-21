# coding=utf-8
from django.db import models
from ..fields import JSONField
from . import EventType, Transport


class NotificationTemplateConfig(models.Model):
    event_type = models.ForeignKey(EventType)
    transport = models.ForeignKey(Transport)
    template_path = models.CharField(max_length=255)
    single_template_path = models.CharField(max_length=255, null=True, blank=True)
    data = JSONField(null=True, blank=True)
    context = models.CharField(max_length=255, default=u'default')

    class Meta:
        app_label = 'notifications'
        unique_together = ('event_type', 'transport', 'context')

    def __unicode__(self):
        return "%s with transport %s uses %s in context %s" % (self.event_type.name, self.transport, self.template_path,
                                                               self.context)


class MultipleNotificationTemplateConfig(models.Model):
    transport = models.ForeignKey(Transport)
    multiple_template_path = models.CharField(max_length=255)
    data = JSONField(null=True, blank=True)
    context = models.CharField(max_length=255, default=u'default')

    class Meta:
        app_label = 'notifications'
        unique_together = ('transport', 'context')

    def __unicode__(self):
        return "Transport %s uses %s in context %s" % (self.transport, self.multiple_template_path, self.context)
