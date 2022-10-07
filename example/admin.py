"""Admin site."""
from django.contrib import admin
from django_admin_filters import DateRange, DateRangePicker, MultiChoice
from .models import Log


class StatusFilter(MultiChoice):
    """Field status filter."""

    FILTER_LABEL = "By status"
    is_collapsed = True


class NumberFilter(MultiChoice):
    """Field number filter."""

    FILTER_LABEL = "By number"


class Timestamp1Filter(DateRange):
    """Field timestamp1 filter."""

    FILTER_LABEL = "By timestamp1"


class Timestamp2Filter(DateRangePicker):
    """Field timestamp2 filter."""

    FILTER_LABEL = "By timestamp2"


class Admin(admin.ModelAdmin):
    """Admin site customization."""

    list_display = ['text', 'status', 'timestamp1', 'timestamp2']
    list_filter = (
      ('status', StatusFilter),
      ('timestamp1', Timestamp1Filter),
      ('timestamp2', Timestamp2Filter),
      ('number', NumberFilter),
    )


admin.site.register(Log, Admin)
