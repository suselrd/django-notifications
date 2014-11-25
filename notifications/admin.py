# coding=utf-8
from django.contrib import admin
from .models import (Action,
                     Event,
                     FeedItem,
                     EventAttendantsConfig,
                     NotificationTemplateConfig,
                     Transport,
                     EventType,
                     EventObjectRole,
                     SubscriptionFrequency,
                     MultipleNotificationTemplateConfig,
                     Subscription,
                     Notification,
                     AttendantRole,
                     DefaultSubscription)
from notifications.models.event import EventTypeCategory


class NotificationTemplateConfigAdmin(admin.ModelAdmin):
    list_filter = ('context', 'transport', 'event_type')


class EventAttendantsConfigAdmin(admin.ModelAdmin):
    list_filter = ('transport', 'event_type')


class EventAttendantsAdminInline(admin.TabularInline):
    model = EventAttendantsConfig
    extra = 0


class NotificationsTemplateConfigAdminInline(admin.TabularInline):
    model = NotificationTemplateConfig
    extra = 0


class EventTypeAdmin(admin.ModelAdmin):
    inlines = [EventAttendantsAdminInline, NotificationsTemplateConfigAdminInline]


admin.site.register(Action)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(EventTypeCategory)
admin.site.register(EventAttendantsConfig, EventAttendantsConfigAdmin)
admin.site.register(NotificationTemplateConfig, NotificationTemplateConfigAdmin)
admin.site.register(MultipleNotificationTemplateConfig)
admin.site.register(Transport)
admin.site.register(EventObjectRole)
admin.site.register(SubscriptionFrequency)
admin.site.register(DefaultSubscription)
admin.site.register(AttendantRole)
#TODO Borrar
admin.site.register(Subscription)
admin.site.register(FeedItem)
admin.site.register(Event)
admin.site.register(Notification)
