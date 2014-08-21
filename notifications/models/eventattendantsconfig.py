# coding=utf-8
from django.db import models
from ..fields import JSONField
from . import EventType, Transport


class EventAttendantsConfig(models.Model):
    event_type = models.ForeignKey(EventType)
    transport = models.ForeignKey(Transport)
    get_attendants_methods = JSONField(null=True, blank=True)

    class Meta:
        app_label = 'notifications'
        unique_together = ('event_type', 'transport')

    def __unicode__(self):
        return "%s in transport %s" % (self.event_type.name, self.transport.name)


class AttendantRole(models.Model):
    role = models.CharField(max_length=200)
    priority = models.IntegerField(default=1)

    class Meta:
        app_label = 'notifications'
        unique_together = ('role',)

    def __unicode__(self):
        return self.role

    @staticmethod
    def get_by_name(name):
        try:
            return AttendantRole.objects.get(role=name)
        except:
            return None
