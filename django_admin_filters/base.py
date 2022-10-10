"""Base class for lib filters."""
from django.contrib import admin


class Base:
    """Mixin class for filters with title, apply button and collapsed state."""

    parameter_name = 'filter'
    title = None

    FILTER_LABEL = "Admin filter"
    BUTTON_LABEL = "Apply"

    def set_title(self):
        """Init title values."""
        self.title = {
          'parameter_name': self.parameter_name,
          'filter_name': self.FILTER_LABEL,
          'button_label': self.BUTTON_LABEL,
        }


class Filter(admin.FieldListFilter, Base):
    """Base class for filters applied to field with title, apply button and collapsed state."""

    parameter_name_mask = 'adminfilter_'

    def __init__(self, field, request, params, model, model_admin, field_path):
        """Customize FieldListFilter functionality."""
        self.parameter_name = self.parameter_name_mask + field_path
        super().__init__(field, request, params, model, model_admin, field_path)
        self.set_title()

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


class FilterSimple(admin.SimpleListFilter, Base):
    """Base class for filters without field with title, apply button and collapsed state."""

    parameter_name = 'adminfilter'
    title = 'Filter'

    def __init__(self, request, params, model, model_admin):
        """Combine parents init."""
        super().__init__(request, params, model, model_admin)
        self.set_title()

    def lookups(self, request, model_admin):
        """Must be implemented in childs."""
        raise NotImplementedError('Method lookups')

    def queryset(self, request, queryset):
        """Must be implemented in childs."""
        raise NotImplementedError('Method queryset')
