"""Admin site."""
from django.contrib import admin
from .models import Log


class Admin(admin.ModelAdmin):
    """Admin site customization."""

    list_display = ['text', 'timestamp1', 'timestamp2']


admin.site.register(Log, Admin)
