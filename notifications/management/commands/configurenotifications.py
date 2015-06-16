# coding=utf-8
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        from ...management import configure_notifications_basics, configure_notifications
        configure_notifications_basics()
        configure_notifications()