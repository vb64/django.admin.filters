"""Admin site."""
from django.contrib import admin
from django_admin_filters import DateRange, DateRangePicker, MultiChoice
from .models import Log


class Admin(admin.ModelAdmin):
    """Admin site customization."""

    list_display = ['text', 'status', 'timestamp1', 'timestamp2']
    list_filter = (
      ('status', MultiChoice),
      ('timestamp1', DateRange),
      ('timestamp2', DateRangePicker)
    )


admin.site.register(Log, Admin)
