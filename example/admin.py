"""Admin site."""
from django.contrib import admin
from django.db.models import Q
from django_admin_filters import DateRange, DateRangePicker, MultiChoice, MultiChoiceExt
from .models import Log


class StatusFilter(MultiChoice):
    """Field status filter."""

    FILTER_LABEL = "By status"


class NumberFilter(MultiChoice):
    """Field number filter."""

    FILTER_LABEL = "By number"


class ColorFilter(MultiChoiceExt):
    """Property color filter."""

    parameter_name = "color"
    FILTER_LABEL = "By color"

    # https://docs.djangoproject.com/en/4.1/topics/db/queries/#complex-lookups-with-q-objects
    options = [
      ('red', 'Red', Q(is_online=False)),
      ('yellow', 'Yellow', Q(is_online=True) & (Q(is_trouble1=True) | Q(is_trouble2=True))),
      ('green', 'Green', Q(is_online=True) & Q(is_trouble1=False) & Q(is_trouble2=False)),
    ]


class Timestamp1Filter(DateRange):
    """Field timestamp1 filter."""

    FILTER_LABEL = "By timestamp1"


class Timestamp2Filter(DateRangePicker):
    """Field timestamp2 filter."""

    FILTER_LABEL = "By timestamp2"


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
      ColorFilter
    )


admin.site.register(Log, Admin)
