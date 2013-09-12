# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Wormhole'
        db.create_table(u'wh_mapper_wormhole', (
            ('sig', self.gf('django.db.models.fields.CharField')(max_length=4, primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('life', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('total_mass', self.gf('django.db.models.fields.BigIntegerField')()),
            ('mass_regen', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('jump_mass', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('static', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'wh_mapper', ['Wormhole'])


    def backwards(self, orm):
        # Deleting model 'Wormhole'
        db.delete_table(u'wh_mapper_wormhole')


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
            'jump_mass': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'life': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'mass_regen': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'sig': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True'}),
            'static': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'total_mass': ('django.db.models.fields.BigIntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        }
    }

    complete_apps = ['wh_mapper']