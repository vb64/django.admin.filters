"""Admin site."""
from django.contrib import admin
from django_admin_filters import DateRange, DateRangePicker
from .models import Log


class MultiChoiceFilter(admin.filters.ChoicesFieldListFilter):
    """Multiselect options filter.

    https://groups.google.com/g/django-users
    https://stackoverflow.com/questions/39790087/is-multi-choice-django-admin-filters-possible

    https://github.com/carltongibson/django-filter

    https://github.com/ctxis/django-admin-multiple-choice-list-filter
    https://github.com/modlinltd/django-advanced-filters
    https://stackoverflow.com/questions/38508672/django-admin-filter-multiple-select
    """


class Admin(admin.ModelAdmin):
    """Admin site customization."""

    list_display = ['text', 'status', 'timestamp1', 'timestamp2']
    list_filter = (
      ('status', MultiChoiceFilter),
      ('timestamp1', DateRange),
      ('timestamp2', DateRangePicker)
    )


admin.site.register(Log, Admin)
