# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from .transport import Transport
from .event import EventType


class SubscriptionFrequency(models.Model):
    name = models.CharField(max_length=100, null=False)
    delta = models.CharField(max_length=100, default='0')

    class Meta:
        app_label = "notifications"

    def __unicode__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User)
    frequency = models.ForeignKey(SubscriptionFrequency, null=True, blank=True, default=1) #TODO
    transport = models.ForeignKey(Transport)
    last_sent = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(EventType, related_name='subs+')

    class Meta:
        app_label = "notifications"

    @staticmethod
    def create_default_subscription(user):
        transports = Transport.objects.all()
        for transport in transports:
            subscription = Subscription(user=user, transport=transport)
            subscription.save()
            event_types = EventType.objects.all().exclude(pk=1)
            for event_type in event_types:
                subscription.items.add(event_type)

    def user_is_subscribed(self, event_type):
        if self.items.filter(pk=event_type.pk).exists():
            return True
        return False

    def __unicode__(self):
        return "USER: %s | TRANSPORT: %s | FREQ: %s" % (self.user.get_full_name() or self.user.username,
                                                        self.transport.name, self.frequency.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.frequency is None:
            self.frequency = SubscriptionFrequency.objects.get(pk=1)
        super(Subscription, self).save(force_insert, force_update, using, update_fields)
