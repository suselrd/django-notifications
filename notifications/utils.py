# coding=utf-8
import logging
from django.utils.module_loading import import_by_path
from notifications.models import AttendantRole

logger = logging.getLogger(__name__)


def get_attendants_from_config(config, event):
    from .models.usereventrelation import UserEventRelation
    attendants = dict()
    if not config:
        return attendants
    try:
        for method in config:
            target = None
            source = method['source']
            if source == 'target_obj':
                target = event.target_object
            elif source == 'related_object':
                target = event.get_related_obj_by_role_name(method['role'])
            elif source == 'event':
                target = event

            if target:
                if 'type' in method and method['type'] == 'function':
                    if hasattr(target, method['value']):
                        attr = getattr(target, method['value'])
                        users = attr()
                else:
                    prop, role = method['value'].split(",")
                    if hasattr(target, prop):
                        users = UserEventRelation(user=getattr(target, prop), role=AttendantRole.get_by_name(role))
            else:
                attendant_method = import_by_path(method['value'])
                users = attendant_method(event)

            #add to the list removing duplicates according to role priority
            check_and_append_user(attendants, users)

    except Exception as e:
        logger.error("Improperly configured attendants methods for action %s with target %s" % (
            event.type.name, event.target_object))

    return attendants


def check_and_append_user(attendants_list, new_attendants):
    if isinstance(new_attendants, list):
        for attendant in new_attendants:
            attendants_list = append_user(attendants_list, attendant)
    else:
        attendants_list = append_user(attendants_list, new_attendants)
    return attendants_list


def append_user(attendants_list, new_attendant):
    if new_attendant.user in attendants_list:
        if attendants_list[new_attendant.user].role.priority > new_attendant.role.priority:
            attendants_list[new_attendant.user] = new_attendant
    else:
        attendants_list[new_attendant.user] = new_attendant
    return attendants_list

