from django.contrib import admin
from .models import discorduser
# Register your models here.
class DiscordUserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'month', 'day')
    search_fields = ['user_id']

admin.site.register(discorduser, DiscordUserAdmin)
