# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'URLAction'
        db.create_table('urlkey_urlaction', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('action_type', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('expired', self.gf('django.db.models.fields.DateTimeField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('onetime', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('data', self.gf('django.db.models.fields.TextField')(default='{}')),
        ))
        db.send_create_signal('urlkey', ['URLAction'])


    def backwards(self, orm):
        # Deleting model 'URLAction'
        db.delete_table('urlkey_urlaction')


    models = {
        'urlkey.urlaction': {
            'Meta': {'ordering': "['-created']", 'object_name': 'URLAction'},
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'default': "'{}'"}),
            'expired': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'onetime': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['urlkey']