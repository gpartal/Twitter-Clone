from django.contrib import admin
from .models import *

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'created_at', 'slug']
    search_fields = ['user__username__icontains', 'name']
    date_hierarchy = 'created_at'
    readonly_fields = ['id', 'slug', 'created_at']
    list_per_page = 15

admin.site.register(Profile, ProfileAdmin)