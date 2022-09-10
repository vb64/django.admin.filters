"""Admin site."""
from django.contrib import admin

from django_admin_filters.daterange import DateRange
from django_admin_filters.daterange_picker import DateRangePicker
from .models import Log

class Admin(admin.ModelAdmin):
    """Admin site customization."""

    list_display = ['text', 'timestamp1', 'timestamp2']
    list_filter = (('timestamp1', DateRange), ('timestamp2', DateRangePicker))


admin.site.register(Log, Admin)
