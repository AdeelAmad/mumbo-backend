from django.contrib import admin
from .models import voicechannelsetting, channel

# Register your models here.

class vcsettingadmin(admin.ModelAdmin):
    list_display = ('guild_id', 'channel_id', 'category', 'bitrate')
    search_fields = ['guild_id__id']

class channeladmin(admin.ModelAdmin):
    list_display = ('guild', 'channel_id', 'owner')
    search_fields = ['guild__guild_id__id']

admin.site.register(voicechannelsetting, vcsettingadmin)
admin.site.register(channel, channeladmin)