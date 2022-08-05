from django.contrib import admin

from .models import levelingsetting, userlevel, rankreward, xpeditevent

# Register your models here.
class levelingsettingadmin(admin.ModelAdmin):
    list_display = ('guild_id', 'global_boost', 'levelupchannel')
    search_fields = ['guild_id__id']

class useradmin(admin.ModelAdmin):
    list_display = ('guild', 'user_id', 'xp', 'last_message')
    search_fields = ['guild__guild_id__id']

class xpediteventadmin(admin.ModelAdmin):
    list_display = ('guild', 'user_id', 'before_xp', 'after_xp', 'timestamp')
    search_fields = ['guild__guild_id__id']

class rankrewardadmin(admin.ModelAdmin):
    list_display = ('guild', 'role_id', 'level')
    search_fields = ['guild__guild_id__id']

admin.site.register(levelingsetting, levelingsettingadmin)
admin.site.register(userlevel, useradmin)
admin.site.register(rankreward, rankrewardadmin)
admin.site.register(xpeditevent, xpediteventadmin)
