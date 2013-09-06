from datetime import datetime
import uuid

from django.db import models

from wh_mapper.constants import NODE_ID_MAX_LENGTH, USERNAME_MAX_LENGTH, \
    SYSTEM_NAME_MAX_LENGTH, SYSTEM_TYPE_MAX_LENGTH, SYSTEM_TYPE_CHOICES, \
    SYSTEM_REGION_MAX_LENGTH, SYSTEM_WSPACE_EFFECT_MAX_LENGTH, \
    SYSTEM_WSPACE_EFFECT_CHOICES, SYSTEM_NODE_PAGE_NAME_MAX_LENGTH, \
    SYSTEM_NODE_NOTES_MAX_LENGTH, WORMHOLE_SIG_MAX_LENGTH, \
    WORMHOLE_LIFE_MAX_LENGTH, WORMHOLE_TOTAL_MASS_MAX_LENGTH, \
    WORMHOLE_JUMP_MASS_MAX_LENGTH


class SystemNode(models.Model):
    id = models.CharField(max_length=NODE_ID_MAX_LENGTH, primary_key=True)
    date = models.DateTimeField()
    author = models.CharField(max_length=USERNAME_MAX_LENGTH)
    name = models.CharField(max_length=SYSTEM_NAME_MAX_LENGTH)
    type = models.CharField(max_length=SYSTEM_TYPE_MAX_LENGTH, choices=SYSTEM_TYPE_CHOICES)
    parent_node = models.ForeignKey('self', null=True)
    page_name = models.CharField(max_length=SYSTEM_NODE_PAGE_NAME_MAX_LENGTH)
    notes = models.CharField(max_length=SYSTEM_NODE_NOTES_MAX_LENGTH)

    def save(self):
        if not self.id:
            self.id = uuid.uuid4().hex
        if not self.date:
            self.date = datetime.now()
        super(SystemNode, self).save()

    def json_safe(self):
        return {'id' : self.id,
                'date' : str(self.date),
                'author' : self.author,
                'name' : self.name,
                'type' : self.get_type_display()}


class System(models.Model):
    name = models.CharField(max_length=SYSTEM_NAME_MAX_LENGTH, primary_key=True)
    type = models.CharField(max_length=SYSTEM_TYPE_MAX_LENGTH, choices=SYSTEM_TYPE_CHOICES)
    region = models.CharField(max_length=SYSTEM_REGION_MAX_LENGTH)
    wspace_effect = models.CharField(max_length=SYSTEM_WSPACE_EFFECT_MAX_LENGTH, choices=SYSTEM_WSPACE_EFFECT_CHOICES)


class Wormhole(models.Model):
    sig = models.CharField(max_length=WORMHOLE_SIG_MAX_LENGTH, primary_key=True)
    type = models.CharField(max_length=SYSTEM_TYPE_MAX_LENGTH, choices=SYSTEM_TYPE_CHOICES)
    #type = models.CharField(max_length=WORMHOLE_TYPE_MAX_LENGTH, choices=WORMHOLE_TYPES)
    life = models.IntegerField(max_length=WORMHOLE_LIFE_MAX_LENGTH)
    total_mass = models.IntegerField(max_length=WORMHOLE_TOTAL_MASS_MAX_LENGTH)
    jump_mass = models.IntegerField(max_length=WORMHOLE_JUMP_MASS_MAX_LENGTH)
