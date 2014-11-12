# coding=utf-8
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.db.models.query import QuerySet
from django.template import loader
from django.utils.translation import ugettext_lazy as _
from .models import Notification, FeedItem, Transport
from . import TRANSPORT_EMAIL


class BaseTransport(object):
    @staticmethod
    def send_notification(user, role, event, template, delay=False):
        raise Exception(_(u'Not implemented!'))

    @staticmethod
    def send_multiple_notification(user, notifications, template, delete_sent=True):
        raise Exception(_(u'Not implemented!'))


class EmailTransport(BaseTransport):
    @staticmethod
    def send_notification(user, role, event, template, delay=False):
        if delay:
            transport = Transport.objects.get(pk=TRANSPORT_EMAIL)
            notification = Notification(user=user, event=event, transport=transport, template_config=template,
                                        sent=False)
            notification.save()
        else:
            context = EmailTransport.create_template_context(user, event.site, role)
            context['subject'] = template.data['subject'] % ({'user': event.user.get_full_name() or event.user.username,
                                                              'target': unicode(event.target_object)})
            context['event'] = event
            EmailTransport.send_mail(context['email'], context['subject'], template.template_path, context)

    @staticmethod
    def send_multiple_notification(user, notifications, template_config, delete_sent=True):

        for site in Site.objects.all():
            site_notifications = notifications.filter(event__site=site)
            if len(site_notifications) == 0:
                continue
            context = EmailTransport.create_template_context(user, site)
            context['subject'] = template_config.data['subject']
            context['notifications'] = site_notifications

            EmailTransport.send_mail(context['email'], context['subject'], template_config.multiple_template_path, context)

        if delete_sent:
            notifications.objects.delete(sent=True)
        else:
            notifications.objects.update(sent=True)

    @staticmethod
    def create_template_context(user, site, role=''):
        email = user.email if isinstance(user, User) else user
        context = {
            'email': email,
            'domain': 'http://' + site.domain,
            'site_name': site.name,
            'user_obj': user,
            'role': role,
        }
        return context

    @staticmethod
    def send_mail(email, subject, template_path, context):
        template_str = loader.render_to_string(template_path, context)
        msg = EmailMessage(subject, template_str, None, [email])
        msg.content_subtype = 'html'  # Main content is now text/html
        msg.send()


class FeedTransport(BaseTransport):
    @staticmethod
    def send_notification(user, role, event, template, delay=False):
        if isinstance(template, list) or isinstance(template, QuerySet):
            for tpl in template:
                FeedTransport._save_feed_item(user, role, event, tpl)
        else:
            FeedTransport._save_feed_item(user, role, event, template)

    @staticmethod
    def _save_feed_item(user, role, event, template):
        feed_item = FeedItem(user=user, role=role, event=event, template_config=template, context=template.context,
                             seen=False, site=event.site)
        feed_item.save()
