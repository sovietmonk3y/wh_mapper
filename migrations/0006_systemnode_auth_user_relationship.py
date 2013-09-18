# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'SystemNode.author' to match new field type.
        db.rename_column(u'wh_mapper_systemnode', 'author', 'author_username')
        # Changing field 'SystemNode.author'
        db.alter_column(u'wh_mapper_systemnode', 'author_username', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], to_field='username', db_column='author_username'))
        # Adding index on 'SystemNode', fields ['author']
        db.create_index(u'wh_mapper_systemnode', ['author_username'])


    def backwards(self, orm):
        # Removing index on 'SystemNode', fields ['author']
        db.delete_index(u'wh_mapper_systemnode', ['author_username'])


        # Renaming column for 'SystemNode.author' to match new field type.
        db.rename_column(u'wh_mapper_systemnode', 'author_username', 'author')
        # Changing field 'SystemNode.author'
        db.alter_column(u'wh_mapper_systemnode', 'author', self.gf('django.db.models.fields.CharField')(max_length=10))

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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'wh_mapper.system': {
            'Meta': {'object_name': 'System'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'wspace_effect': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        u'wh_mapper.systemnode': {
            'Meta': {'object_name': 'SystemNode'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'to_field': "'username'", 'db_column': "'author_username'"}),
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