# coding=utf-8
from django.conf import settings
from django.db.models.signals import post_syncdb
from .. import models as notifications_app
from notifications.models import MultipleNotificationTemplateConfig, EventObjectRole


def configure_notifications_basics(**kwargs):
    from ..models import (
        Transport, Action, EventType, EventTypeCategory, SubscriptionFrequency, DefaultSubscription
    )
    INTERNAL_TRANSPORT_DEFAULT_SUBSCRIPTION = getattr(
        settings,
        'NOTIFICATIONS_INTERNAL_TRANSPORT_DEFAULT_SUBSCRIPTION',
        None
    )
    INTERNAL_TRANSPORT_DEFAULT_SUBSCRIPTION_FREQUENCY = getattr(
        settings,
        'NOTIFICATIONS_INTERNAL_TRANSPORT_DEFAULT_SUBSCRIPTION_FREQUENCY',
        None
    )
    EMAIL_TRANSPORT_DEFAULT_SUBSCRIPTION = getattr(
        settings,
        'NOTIFICATIONS_EMAIL_TRANSPORT_DEFAULT_SUBSCRIPTION',
        None
    )
    EMAIL_TRANSPORT_DEFAULT_SUBSCRIPTION_FREQUENCY = getattr(
        settings,
        'NOTIFICATIONS_EMAIL_TRANSPORT_DEFAULT_SUBSCRIPTION_FREQUENCY',
        None
    )

    internal_transport, created = Transport.objects.get_or_create(
        cls='notifications.transports.FeedTransport',
        defaults={
            'name': 'internal_notifications',
            'allows_context': True,
            'allows_freq_config': False,
            'delete_sent': False,
        }
    )
    email_transport, created = Transport.objects.get_or_create(
        cls='notifications.transports.EmailTransport',
        defaults={
            'name': 'email',
            'allows_context': False,
            'allows_freq_config': True,
            'delete_sent': True,
        }
    )
    default_action, created = Action.objects.get_or_create(
        name='default',
        defaults={
            'read_as': 'Default',
            'description': ''
        }
    )
    default_event_category, created = EventTypeCategory.objects.get_or_create(
        name='default',
        defaults={
            'read_as': 'Default'
        }
    )
    default_event_type, created = EventType.objects.get_or_create(
        name='default',
        defaults={
            'read_as': '',
            'action': default_action,
            'category': default_event_category,
            'target_type': 'all'
        }
    )
    immediate_frequency, created = SubscriptionFrequency.objects.get_or_create(
        name='immediately'
    )
    daily_frequency, created = SubscriptionFrequency.objects.get_or_create(
        name='daily'
    )
    weekly_frequency, created = SubscriptionFrequency.objects.get_or_create(
        name='weekly'
    )

    internal_transport_default_subscription, created = DefaultSubscription.objects.get_or_create(
        transport=internal_transport,
        defaults={
            'frequency': INTERNAL_TRANSPORT_DEFAULT_SUBSCRIPTION_FREQUENCY or immediate_frequency,
        }
    )
    internal_transport_default_subscription.items = EventType.objects.filter(name__in=INTERNAL_TRANSPORT_DEFAULT_SUBSCRIPTION or [default_event_type.name])

    email_transport_default_subscription, created = DefaultSubscription.objects.get_or_create(
        transport=email_transport,
        defaults={
            'frequency': EMAIL_TRANSPORT_DEFAULT_SUBSCRIPTION_FREQUENCY or immediate_frequency,
        }
    )
    email_transport_default_subscription.items = EventType.objects.filter(name__in=EMAIL_TRANSPORT_DEFAULT_SUBSCRIPTION or [default_event_type.name])


post_syncdb.connect(
    configure_notifications_basics,
    sender=notifications_app,
    dispatch_uid='notifications_configure_notifications_basics'
)


def configure_notifications(**kwargs):
    from ..models import (
        Transport,
        Action,
        EventType,
        EventTypeCategory,
        EventAttendantsConfig,
        NotificationTemplateConfig,
        AttendantRole
    )
    NOTIFICATIONS_SETTINGS = getattr(
        settings,
        'NOTIFICATIONS_SETTINGS',
        {}
    )
    transports = NOTIFICATIONS_SETTINGS.setdefault('transports', {})
    for cls, config in transports.items():
        if not Transport.objects.filter(cls=cls).update(**config):
            Transport.objects.create(cls=cls, **config)

    actions = NOTIFICATIONS_SETTINGS.setdefault('actions', {})
    for name, config in actions.items():
        if not Action.objects.filter(name=name).update(**config):
            Action.objects.create(name=name, **config)

    categories = NOTIFICATIONS_SETTINGS.setdefault('event_categories', {})
    for name, info in categories.items():
        if not EventTypeCategory.objects.filter(name=name).update(**info):
            EventTypeCategory.objects.create(name=name, **info)

    attendant_roles = NOTIFICATIONS_SETTINGS.setdefault('attendant_roles', {})
    for role, info in attendant_roles.items():
        if not AttendantRole.objects.filter(role=role).update(**info):
            AttendantRole.objects.create(role=role, **info)

    event_object_roles = NOTIFICATIONS_SETTINGS.setdefault('event_object_roles', [])
    for role in event_object_roles:
        EventObjectRole.objects.get_or_create(name=role)

    multiple_templates = NOTIFICATIONS_SETTINGS.setdefault('multiple_templates', {})
    for transport_key, templates in multiple_templates.items():
        transport = Transport.objects.get_by_natural_key(transport_key)
        for context, template_settings in templates.items():
            MultipleNotificationTemplateConfig.objects.get_or_create(
                transport=transport, context=context, defaults=template_settings
            )

    events = NOTIFICATIONS_SETTINGS.setdefault('events', {})
    for name, event_info in events.items():
        category_key = event_info.get('category', 'default')
        try:
            event_info['category'] = EventTypeCategory.objects.get_by_natural_key(category_key)
        except EventTypeCategory.DoesNotExist:
            event_info.pop('category')

        action_key = event_info.get('action', 'default')
        try:
            event_info['action'] = Action.objects.get_by_natural_key(action_key)
        except Action.DoesNotExist:
            event_info.pop('action')

        notifications = event_info.pop('notifications', {})
        event_type, created = EventType.objects.get_or_create(
            name=name,
            defaults=event_info
        )

        for transport_key, notification_settings in notifications.items():
            transport = Transport.objects.get_by_natural_key(transport_key)
            EventAttendantsConfig.objects.get_or_create(
                event_type=event_type,
                transport=transport,
                defaults={
                    'get_attendants_methods': notification_settings.pop('attendants', [])
                }
            )
            templates_config = notification_settings.pop('templates', {})
            for context, template_config in templates_config.items():
                NotificationTemplateConfig.objects.get_or_create(
                    event_type=event_type,
                    transport=transport,
                    context=context,
                    defaults=template_config
                )


post_syncdb.connect(
    configure_notifications,
    sender=notifications_app,
    dispatch_uid='notifications_configure_notifications'
)