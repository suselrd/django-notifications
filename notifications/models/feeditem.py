# coding=utf-8

from django.contrib.auth.models import User
from django.db import models
from . import NotificationTemplateConfig, Event


class FeedItem(models.Model):
    user = models.ForeignKey(User)
    role = models.CharField(max_length=100, null=True, blank=True)
    event = models.ForeignKey(Event)
    template_config = models.ForeignKey(NotificationTemplateConfig)
    context = models.CharField(default=u'default', max_length=255)
    seen = models.BooleanField(default=False)

    class Meta:
        app_label = 'notifications'
        unique_together = ('user', 'event', 'context')

    def __unicode__(self):
        return "For %s - %s %s - %s" % (
            self.user.get_full_name() or self.user.username, self.event.user.username, self.event.type.name,
            unicode(self.event.target_object))
