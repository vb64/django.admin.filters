"""Base class for lib filters."""
from django.contrib import admin


class Filter(admin.FieldListFilter):
    """Base class for filters with title, apply button and collapsed state."""

    is_collapsed = False
    parameter_name_mask = 'adminfilter_'

    FILTER_LABEL = "Admin filter"
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

    @property
    def collapsed_state(self):
        """Return string for CSS stype."""
        return '' if self.is_collapsed else 'open'

    def value(self):
        """Return the string provided in the request's query string.

        None if the value wasn't provided.
        """
        return self.used_parameters.get(self.parameter_name)

    def expected_parameters(self):
        """Parameter list for chice filter."""
        return [self.parameter_name]

    def choices(self, changelist):
        """Must be implemented in childs."""
        raise NotImplementedError('Method choices')
