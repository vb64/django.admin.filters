"""Django admin multi choice filter with checkboxes for db fields with choices option."""
from django.contrib import admin


class MultiChoice(admin.filters.ChoicesFieldListFilter):
    """Multiselect options filter.

    https://groups.google.com/g/django-users
    https://stackoverflow.com/questions/39790087/is-multi-choice-django-admin-filters-possible

    https://github.com/carltongibson/django-filter

    https://github.com/ctxis/django-admin-multiple-choice-list-filter
    https://github.com/modlinltd/django-advanced-filters
    https://stackoverflow.com/questions/38508672/django-admin-filter-multiple-select

    for lookup, title in self.field.flatchoices:
    """

    template = 'multi_choice.html'
