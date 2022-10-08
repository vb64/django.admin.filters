"""Django admin multi choice filter with checkboxes for db fields with choices option."""
from .base import Filter as BaseFilter


class Filter(BaseFilter):
    """Multi choice options filter.

    For CharField and IntegerField fields with 'choices' option.

    https://stackoverflow.com/questions/39790087/is-multi-choice-django-admin-filters-possible
    https://stackoverflow.com/questions/38508672/django-admin-filter-multiple-select
    https://github.com/ctxis/django-admin-multiple-choice-list-filter
    https://github.com/modlinltd/django-advanced-filters
    """

    template = 'multi_choice.html'
    parameter_name_mask = 'mchoice_'

    FILTER_LABEL = "By choices"
    CHOICES_SEPARATOR = ','

    def __init__(self, field, request, params, model, model_admin, field_path):
        """Extend base functionality."""
        super().__init__(field, request, params, model, model_admin, field_path)

        self.title.update({
          'choices_separator': self.CHOICES_SEPARATOR,
        })
        val = self.value()
        self.selected = val.split(self.CHOICES_SEPARATOR) if val else []
        self.lookup_choices = self.get_lookup_choices()

    def get_lookup_choices(self):
        """Return filter choices."""
        if self.field.get_internal_type() in ['IntegerField']:
            self.selected = [int(i) for i in self.selected]
        return self.field.flatchoices

    def choices(self, changelist):
        """Define filter checkboxes."""
        for lookup, title in self.lookup_choices:
            yield {
              'selected': lookup in self.selected,
              'value': lookup,
              'display': title,
            }

    def queryset(self, request, queryset):
        """Return the filtered by selected options queryset."""
        if self.selected:
            params = {
              "{}__in".format(self.field_path): self.selected,
            }
            return queryset.filter(**params)

        return queryset


class FilterExt(Filter):
    """Extended variant of previous filter, that allows filtering by custom defined properties."""

    options = [
      ('red', 'Red', True),
      ('yellow', 'Yellow', True),
      ('green', 'Green', True),
    ]

    def get_lookup_choices(self):
        """Return filter choices."""
        return [i[:2] for i in self.options]

    def queryset(self, request, queryset):
        """Return the filtered by selected options queryset."""
        return queryset
