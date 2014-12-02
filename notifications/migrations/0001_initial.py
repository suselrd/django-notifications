# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Action'
        db.create_table(u'notifications_action', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('read_as', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal('notifications', ['Action'])

        # Adding model 'Transport'
        db.create_table(u'notifications_transport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('cls', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('allows_freq_config', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allows_context', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('delete_sent', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('notifications', ['Transport'])

        # Adding model 'EventObjectRole'
        db.create_table(u'notifications_eventobjectrole', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('notifications', ['EventObjectRole'])

        # Adding model 'EventType'
        db.create_table(u'notifications_eventtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('read_as', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('action', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.Action'])),
            ('target_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('notifications', ['EventType'])

        # Adding model 'Event'
        db.create_table(u'notifications_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.EventType'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='events', to=orm['auth.User'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('target_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='event', to=orm['contenttypes.ContentType'])),
            ('target_pk', self.gf('django.db.models.fields.TextField')()),
            ('extra_data', self.gf('notifications.fields.JSONField')(null=True, blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')(max_length=500)),
        ))
        db.send_create_signal('notifications', ['Event'])

        # Adding model 'EventObjectRoleRelation'
        db.create_table(u'notifications_eventobjectrolerelation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.Event'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.EventObjectRole'])),
            ('target_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='eventobjectrolerelation', to=orm['contenttypes.ContentType'])),
            ('target_pk', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('notifications', ['EventObjectRoleRelation'])

        # Adding model 'EventAttendantsConfig'
        db.create_table(u'notifications_eventattendantsconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.EventType'])),
            ('transport', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.Transport'])),
            ('get_attendants_methods', self.gf('notifications.fields.JSONField')(null=True, blank=True)),
        ))
        db.send_create_signal('notifications', ['EventAttendantsConfig'])

        # Adding unique constraint on 'EventAttendantsConfig', fields ['event_type', 'transport']
        db.create_unique(u'notifications_eventattendantsconfig', ['event_type_id', 'transport_id'])

        # Adding model 'AttendantRole'
        db.create_table(u'notifications_attendantrole', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('priority', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('notifications', ['AttendantRole'])

        # Adding unique constraint on 'AttendantRole', fields ['role']
        db.create_unique(u'notifications_attendantrole', ['role'])

        # Adding model 'NotificationTemplateConfig'
        db.create_table(u'notifications_notificationtemplateconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.EventType'])),
            ('transport', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.Transport'])),
            ('template_path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('single_template_path', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('data', self.gf('notifications.fields.JSONField')(null=True, blank=True)),
            ('context', self.gf('django.db.models.fields.CharField')(default=u'default', max_length=255)),
        ))
        db.send_create_signal('notifications', ['NotificationTemplateConfig'])

        # Adding unique constraint on 'NotificationTemplateConfig', fields ['event_type', 'transport', 'context']
        db.create_unique(u'notifications_notificationtemplateconfig', ['event_type_id', 'transport_id', 'context'])

        # Adding model 'MultipleNotificationTemplateConfig'
        db.create_table(u'notifications_multiplenotificationtemplateconfig', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('transport', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.Transport'])),
            ('multiple_template_path', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('data', self.gf('notifications.fields.JSONField')(null=True, blank=True)),
            ('context', self.gf('django.db.models.fields.CharField')(default=u'default', max_length=255)),
        ))
        db.send_create_signal('notifications', ['MultipleNotificationTemplateConfig'])

        # Adding unique constraint on 'MultipleNotificationTemplateConfig', fields ['transport', 'context']
        db.create_unique(u'notifications_multiplenotificationtemplateconfig', ['transport_id', 'context'])

        # Adding model 'Notification'
        db.create_table(u'notifications_notification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'notifications', to=orm['auth.User'])),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.Event'])),
            ('transport', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.Transport'])),
            ('template_config', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.NotificationTemplateConfig'])),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('notifications', ['Notification'])

        # Adding unique constraint on 'Notification', fields ['user', 'event']
        db.create_unique(u'notifications_notification', ['user_id', 'event_id'])

        # Adding model 'FeedItem'
        db.create_table(u'notifications_feeditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.Event'])),
            ('template_config', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.NotificationTemplateConfig'])),
            ('context', self.gf('django.db.models.fields.CharField')(default=u'default', max_length=255)),
            ('seen', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('notifications', ['FeedItem'])

        # Adding unique constraint on 'FeedItem', fields ['user', 'event', 'context']
        db.create_unique(u'notifications_feeditem', ['user_id', 'event_id', 'context'])

        # Adding model 'SubscriptionFrequency'
        db.create_table(u'notifications_subscriptionfrequency', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('delta', self.gf('django.db.models.fields.CharField')(default='0', max_length=100)),
        ))
        db.send_create_signal('notifications', ['SubscriptionFrequency'])

        # Adding model 'Subscription'
        db.create_table(u'notifications_subscription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('frequency', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['notifications.SubscriptionFrequency'], null=True, blank=True)),
            ('transport', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['notifications.Transport'])),
            ('last_sent', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('notifications', ['Subscription'])

        # Adding M2M table for field items on 'Subscription'
        m2m_table_name = db.shorten_name(u'notifications_subscription_items')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('subscription', models.ForeignKey(orm['notifications.subscription'], null=False)),
            ('eventtype', models.ForeignKey(orm['notifications.eventtype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['subscription_id', 'eventtype_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'FeedItem', fields ['user', 'event', 'context']
        db.delete_unique(u'notifications_feeditem', ['user_id', 'event_id', 'context'])

        # Removing unique constraint on 'Notification', fields ['user', 'event']
        db.delete_unique(u'notifications_notification', ['user_id', 'event_id'])

        # Removing unique constraint on 'MultipleNotificationTemplateConfig', fields ['transport', 'context']
        db.delete_unique(u'notifications_multiplenotificationtemplateconfig', ['transport_id', 'context'])

        # Removing unique constraint on 'NotificationTemplateConfig', fields ['event_type', 'transport', 'context']
        db.delete_unique(u'notifications_notificationtemplateconfig', ['event_type_id', 'transport_id', 'context'])

        # Removing unique constraint on 'AttendantRole', fields ['role']
        db.delete_unique(u'notifications_attendantrole', ['role'])

        # Removing unique constraint on 'EventAttendantsConfig', fields ['event_type', 'transport']
        db.delete_unique(u'notifications_eventattendantsconfig', ['event_type_id', 'transport_id'])

        # Deleting model 'Action'
        db.delete_table(u'notifications_action')

        # Deleting model 'Transport'
        db.delete_table(u'notifications_transport')

        # Deleting model 'EventObjectRole'
        db.delete_table(u'notifications_eventobjectrole')

        # Deleting model 'EventType'
        db.delete_table(u'notifications_eventtype')

        # Deleting model 'Event'
        db.delete_table(u'notifications_event')

        # Deleting model 'EventObjectRoleRelation'
        db.delete_table(u'notifications_eventobjectrolerelation')

        # Deleting model 'EventAttendantsConfig'
        db.delete_table(u'notifications_eventattendantsconfig')

        # Deleting model 'AttendantRole'
        db.delete_table(u'notifications_attendantrole')

        # Deleting model 'NotificationTemplateConfig'
        db.delete_table(u'notifications_notificationtemplateconfig')

        # Deleting model 'MultipleNotificationTemplateConfig'
        db.delete_table(u'notifications_multiplenotificationtemplateconfig')

        # Deleting model 'Notification'
        db.delete_table(u'notifications_notification')

        # Deleting model 'FeedItem'
        db.delete_table(u'notifications_feeditem')

        # Deleting model 'SubscriptionFrequency'
        db.delete_table(u'notifications_subscriptionfrequency')

        # Deleting model 'Subscription'
        db.delete_table(u'notifications_subscription')

        # Removing M2M table for field items on 'Subscription'
        db.delete_table(db.shorten_name(u'notifications_subscription_items'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'notifications.action': {
            'Meta': {'object_name': 'Action'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'read_as': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'notifications.attendantrole': {
            'Meta': {'unique_together': "(('role',),)", 'object_name': 'AttendantRole'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'notifications.event': {
            'Meta': {'object_name': 'Event'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'extra_data': ('notifications.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'target_pk': ('django.db.models.fields.TextField', [], {}),
            'target_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'event'", 'to': u"orm['contenttypes.ContentType']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.EventType']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'to': u"orm['auth.User']"})
        },
        'notifications.eventattendantsconfig': {
            'Meta': {'unique_together': "(('event_type', 'transport'),)", 'object_name': 'EventAttendantsConfig'},
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.EventType']"}),
            'get_attendants_methods': ('notifications.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'transport': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.Transport']"})
        },
        'notifications.eventobjectrole': {
            'Meta': {'object_name': 'EventObjectRole'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'notifications.eventobjectrolerelation': {
            'Meta': {'object_name': 'EventObjectRoleRelation'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.EventObjectRole']"}),
            'target_pk': ('django.db.models.fields.TextField', [], {}),
            'target_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eventobjectrolerelation'", 'to': u"orm['contenttypes.ContentType']"})
        },
        'notifications.eventtype': {
            'Meta': {'object_name': 'EventType'},
            'action': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.Action']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'read_as': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'target_type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'notifications.feeditem': {
            'Meta': {'unique_together': "(('user', 'event', 'context'),)", 'object_name': 'FeedItem'},
            'context': ('django.db.models.fields.CharField', [], {'default': "u'default'", 'max_length': '255'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'template_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.NotificationTemplateConfig']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'notifications.multiplenotificationtemplateconfig': {
            'Meta': {'unique_together': "(('transport', 'context'),)", 'object_name': 'MultipleNotificationTemplateConfig'},
            'context': ('django.db.models.fields.CharField', [], {'default': "u'default'", 'max_length': '255'}),
            'data': ('notifications.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'multiple_template_path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'transport': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.Transport']"})
        },
        'notifications.notification': {
            'Meta': {'unique_together': "(('user', 'event'),)", 'object_name': 'Notification'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'template_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.NotificationTemplateConfig']"}),
            'transport': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.Transport']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'notifications'", 'to': u"orm['auth.User']"})
        },
        'notifications.notificationtemplateconfig': {
            'Meta': {'unique_together': "(('event_type', 'transport', 'context'),)", 'object_name': 'NotificationTemplateConfig'},
            'context': ('django.db.models.fields.CharField', [], {'default': "u'default'", 'max_length': '255'}),
            'data': ('notifications.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'event_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.EventType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'single_template_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'template_path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'transport': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.Transport']"})
        },
        'notifications.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'frequency': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['notifications.SubscriptionFrequency']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'subs+'", 'symmetrical': 'False', 'to': "orm['notifications.EventType']"}),
            'last_sent': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'transport': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.Transport']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'notifications.subscriptionfrequency': {
            'Meta': {'object_name': 'SubscriptionFrequency'},
            'delta': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'notifications.transport': {
            'Meta': {'object_name': 'Transport'},
            'allows_context': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'allows_freq_config': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cls': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'delete_sent': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['notifications']