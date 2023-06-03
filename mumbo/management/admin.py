from django.contrib import admin
from .models import Guild

# Register your models here.
class GuildAdmin(admin.ModelAdmin):
    list_display = ('id', 'counting', 'voicechannel', 'leveling', 'afkmusic', 'waifu', 'alert', 'migrated')
    list_filter = ('counting', 'voicechannel', 'leveling', 'afkmusic', 'waifu', 'alert', 'migrated')
    search_fields = ['id']

admin.site.register(Guild, GuildAdmin)