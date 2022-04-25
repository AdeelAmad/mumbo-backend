from django.db import models
import sys
sys.path.append('../mumbo')

from management.models import Guild

# Create your models here.
class voicechannelsetting(models.Model):
    guild_id = models.ForeignKey(Guild, on_delete=models.PROTECT)
    channel_id = models.TextField(max_length=18, default="")
    category = models.TextField(max_length=18, default="")
    bitrate = models.IntegerField(default=64)

class channel(models.Model):
    guild = models.ForeignKey(voicechannelsetting, on_delete=models.PROTECT)
    channel_id = models.TextField(max_length=18)
    owner = models.TextField(max_length=18)