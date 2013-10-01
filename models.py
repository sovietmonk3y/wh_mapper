from datetime import datetime
import uuid

from django.contrib.auth.models import User
from django.db import models

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


class SystemNode(models.Model):
    id = models.CharField(max_length=wmc.NODE_ID_MAX_LENGTH, primary_key=True)
    date = models.DateTimeField()
    author = models.ForeignKey(User, to_field='username',
                               db_column='author_username')
    system = models.ForeignKey(System, null=True, db_column='system_name')
    parent_node = models.ForeignKey('self', null=True)
    page_name = models.CharField(
        max_length=wmc.SYSTEM_NODE_PAGE_NAME_MAX_LENGTH)
    notes = models.CharField(max_length=wmc.SYSTEM_NODE_NOTES_MAX_LENGTH)

    def _get_system_name(self):
        return self.system_id
    def _set_system_name(self, value):
        self.system_id = value
    system_name = property(_get_system_name, _set_system_name)

    def _get_author_username(self):
        return self.author_id
    def _set_author_username(self, value):
        self.author_id = value
    author_username = property(_get_author_username, _set_author_username)

    def save(self):
        if not self.id:
            self.id = uuid.uuid4().hex
        if not self.date:
            self.date = datetime.now()
        super(SystemNode, self).save()

    def json_safe(self):
        json_dict = {'id' : self.id,
                     'parent_node_id' : self.parent_node_id,
                     'date' : self.date.strftime('%m/%d/%Y %H:%M:%S'),
                     'author' : self.author_username,
                     'name' : self.system.name,
                     'type' : self.system.type,
                     'region' : self.system.region}

        if not self.system.region and self.system.wspace_effect:
            json_dict['wspace_effect'] = (
                wmc.WSPACE_EFFECTS_HTML[self.system.wspace_effect] %
                wmc.WSPACE_EFFECT_CLASSES[self.system.wspace_effect][
                    self.system.type])

        return json_dict


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
