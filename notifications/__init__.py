# coding=utf-8

TRANSPORT_FEED = 1
TRANSPORT_EMAIL = 2


def create_event(user, event_type, target, details, extra_data=None, related_objects=None):
    from .models import Event, EventObjectRoleRelation
    from .tasks import send_notification
    event = Event(user=user, type=event_type, target_object=target, extra_data=extra_data, details=details)
    event.save()
    if related_objects:
        for role, obj in related_objects.items():
            event_relation_object = EventObjectRoleRelation(event=event, role=role, target_object=obj)
            event_relation_object.save()
    if event_type.immediate:
        send_notification(event)
    else:
        send_notification.delay(event)
