# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'SystemNode.name'
        db.delete_column(u'wh_mapper_systemnode', 'name')

        # Deleting field 'SystemNode.type'
        db.delete_column(u'wh_mapper_systemnode', 'type')

        # Adding field 'SystemNode.system'
        db.add_column(u'wh_mapper_systemnode', 'system',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wh_mapper.System'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'SystemNode.name'
        db.add_column(u'wh_mapper_systemnode', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20),
                      keep_default=False)

        # Adding field 'SystemNode.type'
        db.add_column(u'wh_mapper_systemnode', 'type',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=4),
                      keep_default=False)

        # Deleting field 'SystemNode.system'
        db.delete_column(u'wh_mapper_systemnode', 'system_id')


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
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'page_name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'parent_node': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wh_mapper.SystemNode']", 'null': 'True'}),
            'system': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wh_mapper.System']", 'null': 'True'})
        },
        u'wh_mapper.wormhole': {
            'Meta': {'object_name': 'Wormhole'},
            'jump_mass': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'life': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'sig': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True'}),
            'total_mass': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        }
    }

    complete_apps = ['wh_mapper']