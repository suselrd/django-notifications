# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'EventType.immediate'
        db.add_column(u'notifications_eventtype', 'immediate',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'EventType.immediate'
        db.delete_column(u'notifications_eventtype', 'immediate')


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
        'notifications.defaultsubscription': {
            'Meta': {'unique_together': "(('transport',),)", 'object_name': 'DefaultSubscription'},
            'frequency': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['notifications.SubscriptionFrequency']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'items': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'def_subs+'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['notifications.EventType']"}),
            'transport': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.Transport']"})
        },
        'notifications.event': {
            'Meta': {'object_name': 'Event'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'extra_data': ('notifications.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']", 'null': 'True'}),
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
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.EventTypeCategory']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'immediate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'read_as': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'target_type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'notifications.eventtypecategory': {
            'Meta': {'object_name': 'EventTypeCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'read_as': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'notifications.feeditem': {
            'Meta': {'unique_together': "(('user', 'event', 'context'),)", 'object_name': 'FeedItem'},
            'context': ('django.db.models.fields.CharField', [], {'default': "u'default'", 'max_length': '255'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
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
        'notifications.publicfeeditem': {
            'Meta': {'unique_together': "(('event', 'context'),)", 'object_name': 'PublicFeedItem'},
            'context': ('django.db.models.fields.CharField', [], {'default': "u'default'", 'max_length': '255'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'seen': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sites.Site']"}),
            'template_config': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['notifications.NotificationTemplateConfig']"})
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
        },
        u'sites.site': {
            'Meta': {'ordering': "(u'domain',)", 'object_name': 'Site', 'db_table': "u'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['notifications']