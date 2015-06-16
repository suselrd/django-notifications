# coding=utf-8
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from ..fields import JSONField
from action import Action
from transport import Transport


class EventTypeCategoryManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class EventTypeCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    read_as = models.CharField(max_length=255)

    objects = EventTypeCategoryManager()

    class Meta:
        app_label = 'notifications'
        verbose_name_plural = 'event type categories'

    def __unicode__(self):
        return self.read_as or self.name

    def natural_key(self):
        return self.name,


class EventObjectRoleManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class EventObjectRole(models.Model):
    name = models.CharField(max_length=255)

    objects = EventObjectRoleManager()

    class Meta:
        app_label = 'notifications'

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return self.name,


class EventTypeManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class EventType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    read_as = models.CharField(max_length=255)
    action = models.ForeignKey(Action)
    target_type = models.CharField(max_length=255)
    category = models.ForeignKey(EventTypeCategory, null=True)
    immediate = models.BooleanField(default=False)

    transports = models.ManyToManyField(Transport, through='EventAttendantsConfig', related_name='event_types')

    objects = EventTypeManager()

    class Meta:
        app_label = 'notifications'

    def __unicode__(self):
        return self.read_as or self.name

    def natural_key(self):
        return self.name,


class EventAttendantsConfig(models.Model):
    event_type = models.ForeignKey(EventType, related_name='attendants_configurations')
    transport = models.ForeignKey(Transport, related_name='attendants_configurations')
    get_attendants_methods = JSONField(null=True, blank=True)

    class Meta:
        app_label = 'notifications'
        unique_together = ('event_type', 'transport')

    def __unicode__(self):
        return "%s in transport %s" % (self.event_type.name, self.transport.name)


class AttendantRoleManager(models.Manager):
    def get_by_natural_key(self, role):
        return self.get(role=role)


class AttendantRole(models.Model):
    role = models.CharField(max_length=200, unique=True)
    priority = models.IntegerField(default=1)

    objects = AttendantRoleManager()

    class Meta:
        app_label = 'notifications'

    def __unicode__(self):
        return self.role

    def natural_key(self):
        return self.role,


class Event(models.Model):
    type = models.ForeignKey(EventType)
    user = models.ForeignKey(User, related_name='events')
    date = models.DateTimeField(auto_now_add=True)

    target_type = models.ForeignKey(ContentType, verbose_name=_('target type'), related_name="%(class)s")
    target_pk = models.TextField(_('target ID'))
    target_object = GenericForeignKey(ct_field="target_type", fk_field="target_pk")

    extra_data = JSONField(null=True, blank=True)
    details = models.TextField(max_length=500)

    site = models.ForeignKey(Site, null=True)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        app_label = 'notifications'

    def __unicode__(self):
        return self.details

    def get_related_obj_by_role_name(self, role_name):
        try:
            role = EventObjectRole.objects.get(name=role_name)
            related_objects = self.eventobjectrolerelation_set.filter(role=role)
            if len(related_objects):
                return related_objects[0].target_object
            return None
        except EventObjectRole.DoesNotExist:
            return None


@receiver(pre_save, sender=Event, dispatch_uid='pre_save_event')
def pre_save_handler(instance, **kwargs):
    if not instance.pk and not instance.site_id:
        instance.site_id = getattr(instance.target_object, 'site_id', Site.objects.get_current().pk)


class EventObjectRoleRelation(models.Model):
    event = models.ForeignKey(Event)
    role = models.ForeignKey(EventObjectRole)

    target_type = models.ForeignKey(ContentType, verbose_name=_('target type'), related_name="%(class)s")
    target_pk = models.TextField(_('target ID'))
    target_object = GenericForeignKey(ct_field="target_type", fk_field="target_pk")

    class Meta:
        app_label = 'notifications'

    def __unicode__(self):
        return self.target_object

