from django.db import models

# Create your models here.
class discorduser(models.Model):
    user_id = models.TextField(max_length=18)
    month = models.IntegerField(default=0)
    day = models.IntegerField(default=0)
    dms = models.BooleanField(default=True)
