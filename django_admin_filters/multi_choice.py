"""Django admin multi choice filter with checkboxes for db fields with choices option."""
from django.contrib import admin
from .mixin import Collapsed


class MultiChoice(admin.filters.ChoicesFieldListFilter, Collapsed):
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
    parameter_name_mask = 'choice_'

    FILTER_LABEL = "Your choice"
    BUTTON_LABEL = "Apply"

    def __init__(self, field, request, params, model, model_admin, field_path):
        """Customize FieldListFilter functionality."""
        self.parameter_name = self.parameter_name_mask + field_path
        super().__init__(field, request, params, model, model_admin, field_path)

        self.title = {
          'parameter_name': self.parameter_name,
          'filter_name': self.FILTER_LABEL,
          'button_label': self.BUTTON_LABEL,
          'collapsed': self.collapsed_state,
        }
