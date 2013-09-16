from datetime import datetime
import uuid

from django.db import models

import wh_mapper.constants as wmc

class System(models.Model):
    name = models.CharField(max_length=wmc.SYSTEM_NAME_MAX_LENGTH, primary_key=True)
    type = models.CharField(max_length=wmc.SYSTEM_TYPE_MAX_LENGTH, choices=wmc.SYSTEM_TYPE_CHOICES)
    region = models.CharField(max_length=wmc.SYSTEM_REGION_MAX_LENGTH)
    wspace_effect = models.CharField(max_length=wmc.SYSTEM_WSPACE_EFFECT_MAX_LENGTH, choices=wmc.SYSTEM_WSPACE_EFFECT_CHOICES)


class SystemNode(models.Model):
    id = models.CharField(max_length=wmc.NODE_ID_MAX_LENGTH, primary_key=True)
    date = models.DateTimeField()
    author = models.CharField(max_length=wmc.USERNAME_MAX_LENGTH)
    system = models.ForeignKey(System, null=True)
    parent_node = models.ForeignKey('self', null=True)
    page_name = models.CharField(max_length=wmc.SYSTEM_NODE_PAGE_NAME_MAX_LENGTH)
    notes = models.CharField(max_length=wmc.SYSTEM_NODE_NOTES_MAX_LENGTH)

    def save(self):
        if not self.id:
            self.id = uuid.uuid4().hex
        if not self.date:
            self.date = datetime.now()
        super(SystemNode, self).save()

    def json_safe(self):
        json_dict = {'id' : self.id,
                     'date' : str(self.date),
                     'author' : self.author,
                     'name' : self.system.name,
                     'type' : self.system.type,
                     'region' : self.system.region}

        if not self.system.region and self.system.wspace_effect:
            json_dict['wspace_effect'] = (
                wmc.WSPACE_EFFECTS_HTML[self.system.wspace_effect] %
                wmc.WSPACE_EFFECT_CLASSES[self.system.wspace_effect][self.system.type])

        return json_dict


class Wormhole(models.Model):
    sig = models.CharField(max_length=wmc.WORMHOLE_SIG_MAX_LENGTH, primary_key=True)
    type = models.CharField(max_length=wmc.SYSTEM_TYPE_MAX_LENGTH, choices=wmc.SYSTEM_TYPE_CHOICES)
    life = models.PositiveSmallIntegerField()
    total_mass = models.BigIntegerField()
    mass_regen = models.PositiveIntegerField()
    jump_mass = models.PositiveIntegerField()
    static = models.BooleanField()
