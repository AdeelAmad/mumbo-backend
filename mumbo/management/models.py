from django.db import models

# Create your models here.
class Guild(models.Model):
    id = models.BigIntegerField(primary_key=True)
    counting = models.BooleanField(default=False)
    voicechannel = models.BooleanField(default=False)
    leveling = models.BooleanField(default=False)
    afkmusic = models.BooleanField(default=False)
    alert = models.BooleanField(default=True)
