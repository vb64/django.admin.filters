"""Django admin multi choice filter with checkboxes for db fields with choices option."""
from .base import Filter as BaseFilter


class Choices:
    """Multi choice options filter."""

    template = 'multi_choice.html'
    selected = []
    lookup_choices = []

    FILTER_LABEL = "By choices"
    CHOICES_SEPARATOR = ','

    def set_selected(self, val, title):
        """Init choices according request parameter string."""
        title.update({
          'choices_separator': self.CHOICES_SEPARATOR,
        })
        self.selected = val.split(self.CHOICES_SEPARATOR) if val else []
        self.lookup_choices = self.get_lookup_choices()

    def get_lookup_choices(self):
        """Return filter choices."""
        return []

    def choices(self, _changelist):
        """Define filter checkboxes."""
        for lookup, title in self.lookup_choices:
            yield {
              'selected': lookup in self.selected,
              'value': lookup,
              'display': title,
            }


class Filter(BaseFilter, Choices):
    """Multi choice options filter.

    For CharField and IntegerField fields with 'choices' option.

    https://stackoverflow.com/questions/39790087/is-multi-choice-django-admin-filters-possible
    https://stackoverflow.com/questions/38508672/django-admin-filter-multiple-select
    https://github.com/ctxis/django-admin-multiple-choice-list-filter
    https://github.com/modlinltd/django-advanced-filters
    """

    parameter_name_mask = 'mchoice_'

    def __init__(self, field, request, params, model, model_admin, field_path):
        """Extend base functionality."""
        super().__init__(field, request, params, model, model_admin, field_path)
        self.set_selected(self.value(), self.title)

    def choices(self, changelist):
        """Call shared implementation."""
        return Choices.choices(self, changelist)

    def get_lookup_choices(self):
        """Return filter choices."""
        if self.field.get_internal_type() in ['IntegerField']:
            self.selected = [int(i) for i in self.selected]
        return self.field.flatchoices

    def queryset(self, request, queryset):
        """Return the filtered by selected options queryset."""
        if self.selected:
            params = {
              "{}__in".format(self.field_path): self.selected,
            }
            return queryset.filter(**params)

        return queryset


class FilterExt(Filter):
    """Allows filtering by custom defined properties."""

    options = []

    def get_lookup_choices(self):
        """Return filter choices."""
        return [i[:2] for i in self.options]

    def queryset(self, request, queryset):
        """Return the filtered by selected options queryset."""
        if not self.selected:
            return queryset

        filters = {i[0]: i[2] for i in self.options}
        qflt = filters[self.selected[0]]
        for item in self.selected[1:]:
            qflt |= filters[item]

        return queryset.filter(qflt)
