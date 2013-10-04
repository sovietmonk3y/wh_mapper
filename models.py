from datetime import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models
import django.utils.html as django_html

import wh_mapper.constants as wmc

class System(models.Model):
    name = models.CharField(max_length=wmc.SYSTEM_NAME_MAX_LENGTH,
                            primary_key=True)
    type = models.CharField(max_length=wmc.SYSTEM_TYPE_MAX_LENGTH,
                            choices=wmc.SYSTEM_TYPE_CHOICES)
    region = models.CharField(max_length=wmc.SYSTEM_REGION_MAX_LENGTH)
    wspace_effect = models.CharField(
        max_length=wmc.SYSTEM_WSPACE_EFFECT_MAX_LENGTH,
        choices=wmc.SYSTEM_WSPACE_EFFECT_CHOICES)


class Wormhole(models.Model):
    sig = models.CharField(max_length=wmc.WORMHOLE_SIG_MAX_LENGTH,
                           primary_key=True)
    type = models.CharField(max_length=wmc.SYSTEM_TYPE_MAX_LENGTH,
                            choices=wmc.SYSTEM_TYPE_CHOICES)
    life = models.PositiveSmallIntegerField()
    total_mass = models.BigIntegerField()
    mass_regen = models.PositiveIntegerField()
    jump_mass = models.PositiveIntegerField()
    static = models.BooleanField()


class MapObject(models.Model):
    id = models.CharField(max_length=wmc.MAP_OBJECT_ID_MAX_LENGTH,
                          primary_key=True)
    date = models.DateTimeField()
    author = models.ForeignKey(User, to_field='username',
                               db_column='author_username')

    def _get_author_username(self):
        return self.author_id
    def _set_author_username(self, value):
        self.author_id = value
    author_username = property(_get_author_username, _set_author_username)

    class Meta:
        abstract = True

    def save(self):
        if not self.id:
            self.id = uuid.uuid4().hex
        if not self.date:
            self.date = datetime.now()
        super(MapObject, self).save()

    def json_safe(self):
        return {'id' : self.id,
                'date' : self.date.strftime('%m/%d/%Y %H:%M:%S'),
                'author' : self.author_username}


class SystemConnection(MapObject):
    parent_celestial = models.PositiveSmallIntegerField(null=True)
    child_celestial = models.PositiveSmallIntegerField(null=True)
    wormhole = models.ForeignKey(Wormhole, db_column='wormhole_sig')
    life_level = models.PositiveSmallIntegerField(
        choices=wmc.WORMHOLE_LIFE_LEVELS)
    mass_level = models.PositiveSmallIntegerField(
        choices=wmc.WORMHOLE_MASS_LEVELS)
    facing_down = models.BooleanField()

    def _get_wormhole_sig(self):
        return self.wormhole_id
    def _set_wormhole_sig(self, value):
        self.wormhole_id = value
    wormhole_sig = property(_get_wormhole_sig, _set_wormhole_sig)

    def json_safe(self):
        json_dict = super(SystemConnection, self).json_safe()
        json_dict.update(parent_celestial=self.parent_celestial,
                         child_celestial=self.child_celestial,
                         wormhole_sig=self.wormhole_sig,
                         life_level=self.life_level,
                         mass_level=self.mass_level,
                         facing_down=self.facing_down)
        return json_dict


class SystemNode(MapObject):
    system = models.ForeignKey(System, null=True, db_column='system_name')
    page_name = models.CharField(
        max_length=wmc.SYSTEM_NODE_PAGE_NAME_MAX_LENGTH)
    parent_node = models.ForeignKey('self', null=True)
    parent_connection = models.ForeignKey(SystemConnection, null=True)
    notes = models.CharField(max_length=wmc.SYSTEM_NODE_NOTES_MAX_LENGTH)

    def _get_system_name(self):
        return self.system_id
    def _set_system_name(self, value):
        self.system_id = value
    system_name = property(_get_system_name, _set_system_name)

    def json_safe(self):
        json_dict = super(SystemNode, self).json_safe()
        json_dict.update(parent_node_id=self.parent_node_id,
                         notes_text=self.notes,
                         notes_html=django_html.linebreaks(self.notes))

        if self.system:
            json_dict.update(name=self.system.name, type=self.system.type,
                             region=self.system.region)

            if not self.system.region and self.system.wspace_effect:
                json_dict['wspace_effect'] = (
                    wmc.WSPACE_EFFECTS_HTML[self.system.wspace_effect] %
                    wmc.WSPACE_EFFECT_CLASSES[self.system.wspace_effect][
                        self.system.type])
        else:
            json_dict.update(name=None, type=None, region=None)

            if (self.parent_connection and
                self.parent_connection.wormhole.sig != 'K162'):
                json_dict['type'] = self.parent_connection.wormhole.type

        if self.parent_connection:
            json_dict['parent_connection'] = self.parent_connection.json_safe()
        else:
            json_dict['parent_connection'] = None

        return json_dict
