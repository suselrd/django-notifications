# coding=utf-8

from django.contrib.auth.models import User
from django.db import models
from . import Event, NotificationTemplateConfig, Transport


class Notification(models.Model):
    user = models.ForeignKey(User, related_name=u'notifications')
    event = models.ForeignKey(Event)
    transport = models.ForeignKey(Transport)
    template_config = models.ForeignKey(NotificationTemplateConfig)
    sent = models.BooleanField(default=False)

    class Meta:
        app_label = 'notifications'
        unique_together = ('user', 'event')

    def __unicode__(self):
        return "For %s - %s %s - %s" % (self.user.get_full_name() or self.user.username, self.event.user.username,
                                        self.event.type.name, unicode(self.event.target_object))
