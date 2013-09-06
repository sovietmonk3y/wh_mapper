# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SystemNode'
        db.create_table(u'wh_mapper_systemnode', (
            ('id', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('parent_node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wh_mapper.SystemNode'], null=True)),
            ('page_name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('notes', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal(u'wh_mapper', ['SystemNode'])

        # Adding model 'System'
        db.create_table(u'wh_mapper_system', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('wspace_effect', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'wh_mapper', ['System'])


    def backwards(self, orm):
        # Deleting model 'SystemNode'
        db.delete_table(u'wh_mapper_systemnode')

        # Deleting model 'System'
        db.delete_table(u'wh_mapper_system')


    models = {
        u'wh_mapper.system': {
            'Meta': {'object_name': 'System'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'wspace_effect': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'wh_mapper.systemnode': {
            'Meta': {'object_name': 'SystemNode'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'page_name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'parent_node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wh_mapper.SystemNode']", 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        }
    }

    complete_apps = ['wh_mapper']