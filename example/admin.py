"""Admin site."""
from django.contrib import admin
from django_admin_filters import DateRange, DateRangePicker, MultiChoice, MultiChoiceExt
from .models import Log


class StatusFilter(MultiChoice):
    """Field status filter."""

    FILTER_LABEL = "By status"
    is_collapsed = True


class NumberFilter(MultiChoice):
    """Field number filter."""

    FILTER_LABEL = "By number"
    is_collapsed = True


class ColorFilter(MultiChoiceExt):
    """Property color filter."""

    FILTER_LABEL = "By color"
    is_collapsed = True


class Timestamp1Filter(DateRange):
    """Field timestamp1 filter."""

    FILTER_LABEL = "By timestamp1"
    is_collapsed = True


class Timestamp2Filter(DateRangePicker):
    """Field timestamp2 filter."""

    FILTER_LABEL = "By timestamp2"
    is_collapsed = True


class Admin(admin.ModelAdmin):
    """Admin site customization."""

    list_display = [
      'text',
      'status',
      'timestamp1', 'timestamp2',
      'is_online', 'is_trouble1', 'is_trouble2', 'color'
    ]
    list_filter = (
      ('status', StatusFilter),
      ('timestamp1', Timestamp1Filter),
      ('timestamp2', Timestamp2Filter),
      ('number', NumberFilter),
      ('is_online', ColorFilter),
    )


admin.site.register(Log, Admin)
