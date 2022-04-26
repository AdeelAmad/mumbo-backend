from django.db import models
import sys
sys.path.append('../mumbo')

from management.models import Guild


# Create your models here.
class levelingsetting(models.Model):
    guild_id = models.ForeignKey(Guild, on_delete=models.PROTECT)
    global_boost = models.FloatField(default=1.0)

class userlevel(models.Model):
    guild = models.ForeignKey(levelingsetting, on_delete=models.PROTECT)
    user_id = models.TextField(max_length=18)
    xp = models.BigIntegerField()