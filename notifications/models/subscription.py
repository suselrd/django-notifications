# coding=utf-8
from django.db import models
from django.contrib.auth.models import User
from event import EventType
from transport import Transport


class SubscriptionFrequencyManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class SubscriptionFrequency(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    delta = models.CharField(max_length=100, default='0')

    objects = SubscriptionFrequencyManager()

    class Meta:
        app_label = "notifications"
        verbose_name_plural = 'subscription frequencies'

    def __unicode__(self):
        return self.name

    def natural_key(self):
        return self.name,


class Subscription(models.Model):
    user = models.ForeignKey(User)
    frequency = models.ForeignKey(SubscriptionFrequency, null=True, blank=True, default=1)  # TODO
    transport = models.ForeignKey(Transport, limit_choices_to={'allows_subscription': True})
    last_sent = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(EventType, related_name='subs+')

    class Meta:
        app_label = "notifications"

    @staticmethod
    def create_default_subscription(user):
        transports = Transport.objects.filter(allows_subscription=True)
        for transport in transports:
            try:
                default_subscription = DefaultSubscription.objects.get(transport=transport)
                subscription = Subscription(user=user, transport=transport, frequency=default_subscription.frequency)
                event_types = default_subscription.items.all()
            except:
                subscription = Subscription(user=user, transport=transport)
                event_types = EventType.objects.all().exclude(pk=1)

            subscription.save()

            for event_type in event_types:
                subscription.items.add(event_type)

    def user_is_subscribed(self, event_type):
        if self.items.filter(pk=event_type.pk).exists():
            return True
        return False

    def __unicode__(self):
        return u"USER: %s | TRANSPORT: %s | FREQ: %s" % (
            self.user.get_full_name() or self.user.username,
            self.transport.name,
            self.frequency.name
        )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.frequency is None:
            self.frequency = SubscriptionFrequency.objects.get(pk=1)
        super(Subscription, self).save(force_insert, force_update, using, update_fields)


class DefaultSubscription(models.Model):
    transport = models.ForeignKey(Transport, limit_choices_to={'allows_subscription': True}, unique=True)
    frequency = models.ForeignKey(SubscriptionFrequency, null=True, blank=True, default=1)  # TODO
    items = models.ManyToManyField(EventType, related_name='def_subs+', null=True, blank=True)

    class Meta:
        app_label = "notifications"

    def __unicode__(self):
        return u"TRANSPORT: %s" % self.transport.name
