from django.contrib import admin
from .models import Count
# Register your models here.

class CountAdmin(admin.ModelAdmin):
    list_display = ('guild_id', 'channel', 'last_count', 'last_counter')
    search_fields = ['guild_id__id']

admin.site.register(Count, CountAdmin)