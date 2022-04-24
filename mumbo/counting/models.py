from django.db import models
import sys
sys.path.append('../mumbo')

from management.models import Guild

# Create your models here.
class Count(models.Model):
    guild_id = models.ForeignKey(Guild, on_delete=models.PROTECT)
    channel = models.TextField(max_length=18, default="")
    last_count = models.IntegerField(default=0)
    last_counter = models.TextField(max_length=18, default="")