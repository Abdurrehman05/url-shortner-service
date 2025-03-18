from django.contrib import admin
from .models import URL

@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    list_display = ['short_url', 'long_url', 'created_at', 'last_accessed', 'access_count', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['short_url', 'long_url']
    readonly_fields = ['created_at', 'last_accessed', 'access_count']
    ordering = ['-created_at']
