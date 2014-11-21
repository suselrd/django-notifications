# coding=utf-8

from django.contrib.auth.models import User
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db import models
from .event import Event
from .notificationtemplateconfig import NotificationTemplateConfig


class PublicFeedItem(models.Model):
    event = models.ForeignKey(Event)
    template_config = models.ForeignKey(NotificationTemplateConfig)
    context = models.CharField(default=u'default', max_length=255)
    seen = models.BooleanField(default=False)

    site = models.ForeignKey(Site)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    def __init__(self, *args, **kwargs):
        super(PublicFeedItem, self).__init__(*args, **kwargs)
        if not self.pk and not self.site_id:
            self.site_id = self.event.site_id or Site.objects.get_current().pk

    class Meta:
        app_label = 'notifications'
        unique_together = ('event', 'context')

    def __unicode__(self):
        return "%s - %s" % (self.event.type.name, unicode(self.event.target_object))
