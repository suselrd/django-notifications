# coding=utf-8
import logging
from notifications import create_event
from notifications.models import (
    EventType,
    Action,
    EventTypeCategory,
    Transport,
    EventAttendantsConfig,
    NotificationTemplateConfig
)

logger = logging.getLogger(__name__)


"""
EXAMPLE_NOTIFICATIONS_VALUE = {
    'notifications.transports.FeedTransport': {
        'attendants': [
            {
                'source': 'target_obj',
                'type': 'property',
                'value': 'owner,owner'
            },
            {
                'source': 'event',
                'value': 'user,acting_user'
            },
            {
                'source': '',
                'value': 'my_app.utils.user_followers'
            }
        ],
        'templates': {
            'primary_context': {
                'single_template_path': None,
                'data': None,
                'template_path': 'notifications/feed/primary_context/action.html'
            },
            'secondary_context': {
                'single_template_path': None,
                'data': None,
                'template_path': 'notifications/feed/secondary_context/action.html'
            }
        }

    },
    'notifications.transports.EmailTransport': {
        'attendants': [
            {
                'source': 'target_obj',
                'type': 'property',
                'value': 'owner,owner'
            }
        ],
        'templates': {
            'email': {
                'single_template_path': 'notifications/email/single/action.html',
                'data': {
                    'subject': '%(user)s ha interactuado con %(target)s'
                },
                'template_path': 'notifications/email/action.html'
            }
        }
    }
}
"""


def notifier(
        event_name,
        read_as=None,
        action_name='default',
        target_type='all',
        event_category='default',
        notifications=None,
        event_immediate=False,
        action_details=None,
        category_details=None
):
    """
    The decorated function must return either a tuple or a dict, containing:
        user: the acting user,
        target: the target object,
        details: text details for the event to be created,
        extra_data [optional],
        related_objects [optional]

    ** In case of a tuple, of course, the order is critical!

    """
    try:
        action = Action.objects.get_by_natural_key(action_name)
        if action_details:
            action.read_as = action_details.get('read_as', action.read_as)
            action.description = action_details.get('description', action.description)
            action.save()
    except Action.DoesNotExist:
        action = Action.objects.create(
            name=action_name,
            read_as=action_details.get('read_as', action_name) if action_details else action_name,
            description=action_details.get('description', '') if action_details else '',
        )
    except Exception as e:
        logger.exception(e)
        action = None
    try:
        category = EventTypeCategory.objects.get_by_natural_key(event_category)
        if category_details:
            category.read_as = category_details.get('read_as', category.read_as)
            category.save()
    except EventTypeCategory.DoesNotExist:
        category = EventTypeCategory.objects.create(
            name=event_category,
            read_as=category_details.get('read_as', event_category) if category_details else event_category,
        )
    except Exception as e:
        logger.exception(e)
        category = None
    try:
        event_type = EventType.objects.get_by_natural_key(event_name)
        if read_as:
            event_type.read_as = read_as
        if action_name:
            event_type.action = action
        if event_category:
            event_type.category = category
        if event_immediate:
            event_type.immediate = event_immediate
        event_type.save()
    except EventType.DoesNotExist:
        event_type = EventType.objects.create(
            name=event_name,
            read_as=read_as or event_name,
            action=action,
            target_type=target_type,
            category=category,
            immediate=event_immediate
        )
    except Exception as e:
        logger.exception(e)
        event_type = None

    if action and category and event_type:
        notifications = notifications or {}
        for transport, settings in notifications.items():
            try:
                transport = Transport.objects.get_by_natural_key(transport)
            except Transport.DoesNotExist:
                continue

            attendants = settings.setdefault('attendants', [])
            if not EventAttendantsConfig.objects.filter(
                event_type=event_type,
                transport=transport,
            ).update(get_attendants_methods=attendants):
                EventAttendantsConfig.objects.create(
                    event_type=event_type,
                    transport=transport,
                    get_attendants_methods=attendants
                )

            templates = settings.setdefault('templates', {})
            for context, templates_settings in templates.items():
                if not NotificationTemplateConfig.objects.filter(
                    event_type=event_type,
                    transport=transport,
                    context=context
                ).update(**templates_settings):
                    NotificationTemplateConfig.objects.create(
                        event_type=event_type,
                        transport=transport,
                        context=context,
                        **templates_settings
                    )

    def decorator(func):
        def func_wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if isinstance(result, tuple):
                result = list(result)
                result.insert(1, event_type)
                create_event(*result)
            elif isinstance(result, dict):
                result.update({'event_type': event_type})
                create_event(**result)
            else:
                logger.error(
                    'Skipping event creation because incorrect arguments were provided by the decorated function.'
                )
        return func_wrapper
    return decorator
