from __future__ import unicode_literals
from django.utils import timezone

from django.db import models

# Create your models here.
class World(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)


class Visitor(models.Model):
    handle = models.TextField()
    # Avatar / Toon in the future

class Message(models.Model):
    world = models.ForeignKey(World, related_name='messages')
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime("%Y-%m-%d %H:%M:%S")