# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('E175', 'c4', 16, 2000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('X877', 'c4', 16, 2000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('O477', 'c3', 16, 2000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('T405', 'c4', 16, 2000000000, 0, 300000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('U574', 'c6', 24, 3000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('H900', 'c5', 24, 3000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('O128', 'c4', 24, 1000000000, 100000000, 300000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('Z060', 'null', 24, 1000000000, 0, 20000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('X702', 'c3', 24, 1000000000, 0, 300000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('Y790', 'c1', 16, 500000000, 0, 20000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('N770', 'c5', 24, 3000000000, 0, 300000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('D792', 'high', 24, 3000000000, 0, 1000000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('B449', 'high', 16, 2000000000, 0, 1000000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('A239', 'low', 24, 2000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('N062', 'c5', 24, 3000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('O883', 'c3', 16, 1000000000, 0, 20000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('R474', 'c6', 24, 3000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('L614', 'c5', 24, 1000000000, 0, 20000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('L477', 'c3', 16, 2000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('G024', 'c2', 16, 2000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('M267', 'c3', 16, 1000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('S804', 'c6', 24, 1000000000, 0, 20000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('N110', 'high', 24, 1000000000, 0, 20000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('Z142', 'null', 24, 3000000000, 0, 1350000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('H121', 'c1', 16, 500000000, 0, 20000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('C391', 'low', 24, 5000000000, 500000000, 1800000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('B274', 'high', 24, 2000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('C248', 'null', 24, 5000000000, 500000000, 1800000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('M609', 'c4', 16, 1000000000, 0, 20000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('S199', 'null', 24, 3000000000, 0, 1350000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('U210', 'low', 24, 3000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('B041', 'c6', 48, 5000000000, 500000000, 300000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('D845', 'high', 24, 5000000000, 500000000, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('A641', 'high', 16, 2000000000, 0, 1000000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('R943', 'c2', 16, 750000000, 0, 300000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('S047', 'high', 24, 3000000000, 0, 300000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('B520', 'high', 24, 5000000000, 500000000, 300000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('R051', 'low', 16, 3000000000, 0, 1000000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('C140', 'low', 24, 3000000000, 0, 1350000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('U319', 'c6', 48, 3000000000, 500000000, 1350000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('Z971', 'c1', 16, 100000000, 0, 20000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('Z457', 'c4', 16, 2000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('N432', 'c5', 24, 3000000000, 0, 1350000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('V753', 'c6', 24, 3000000000, 0, 1350000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('N766', 'c2', 16, 2000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('K329', 'null', 24, 5000000000, 500000000, 1800000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('K346', 'null', 24, 3000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('P060', 'c1', 16, 500000000, 0, 20000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('N944', 'low', 24, 3000000000, 0, 1350000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('Y683', 'c4', 16, 2000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('V283', 'null', 24, 3000000000, 0, 1000000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('V301', 'c1', 16, 500000000, 0, 20000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('N968', 'c3', 16, 2000000000, 0, 300000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('Q317', 'c1', 16, 500000000, 0, 20000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('I182', 'c2', 16, 2000000000, 0, 300000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('Z647', 'c1', 16, 500000000, 0, 20000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('C247', 'c3', 16, 2000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('H296', 'c5', 24, 3000000000, 0, 1350000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('D364', 'c2', 16, 1000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('N290', 'low', 24, 3000000000, 500000000, 1350000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('W237', 'c6', 24, 3000000000, 0, 1350000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('A982', 'c6', 24, 3000000000, 0, 300000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('V911', 'c5', 24, 3000000000, 0, 1350000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('J244', 'low', 24, 1000000000, 0, 20000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('M555', 'c5', 24, 3000000000, 0, 1000000000, 0);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('D382', 'c2', 16, 2000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('E545', 'null', 24, 2000000000, 0, 300000000, 1);")
        db.execute("INSERT INTO wh_mapper_wormhole (sig, type, life, total_mass, mass_regen, jump_mass, static) VALUES ('C125', 'c2', 16, 1000000000, 0, 20000000, 0);")

    def backwards(self, orm):
        db.execute("DELETE FROM wh_mapper_wormhole;")

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
            'mass_regen': ('django.db.models.fields.IntegerField', [], {'max_length': '9'}),
            'sig': ('django.db.models.fields.CharField', [], {'max_length': '4', 'primary_key': 'True'}),
            'static': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'total_mass': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        }
    }

    complete_apps = ['wh_mapper']
    symmetrical = True
