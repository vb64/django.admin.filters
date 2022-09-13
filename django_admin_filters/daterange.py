"""Django admin daterange filter with simple inputs and shortcuts."""
from datetime import datetime, timedelta
from django.contrib import admin

HOUR_SECONDS = 60 * 60
DAY_SECONDS = HOUR_SECONDS * 24

KEY_SELECTED = 'selected'
KEY_QUERY = 'query_string'
KEY_DISPLAY = 'display'


class DateRange(admin.FieldListFilter):
    """Date range filter with input fields."""

    FILTER_LABEL = "Data range"
    FROM_LABEL = "From"
    TO_LABEL = "To"
    ALL_LABEL = 'All'
    CUSTOM_LABEL = "custom range"
    NULL_LABEL = "no date"
    BUTTON_LABEL = "Set range"
    DATE_FORMAT = "YYYY-MM-DD HH:mm"
    INITIAL_START = ''
    INITIAL_END = ''

    WRONG_OPTION_VALUE = -DAY_SECONDS
    is_null_option = True

    options = (
      ('1da', "24 hours ahead", DAY_SECONDS),
      ('1dp', "24 hours in the past", -DAY_SECONDS),
    )

    template = 'daterange.html'

    parameter_name_mask = 'range_'
    parameter_start_mask = 'start_'
    parameter_end_mask = 'end_'

    option_custom = 'custom'
    option_null = 'empty'

    def __init__(self, field, request, params, model, model_admin, field_path):
        """Unite FieldListFilter and SimpleListFilter functionality."""
        self.parameter_name = self.parameter_name_mask + field_path
        self.parameter_start = self.parameter_start_mask + field_path
        self.parameter_end = self.parameter_end_mask + field_path

        super().__init__(field, request, params, model, model_admin, field_path)

        self.lookup_choices = list(self.lookups(request, model_admin))
        self.interval = {i[0]: i[2] for i in self.options}

        self.title = {
          'parameter_name': self.parameter_name,
          'parameter_start': self.parameter_start,
          'parameter_end': self.parameter_end,
          'option_custom': self.option_custom,
          'filter_name': self.FILTER_LABEL,
          'start_label': self.FROM_LABEL,
          'end_label': self.TO_LABEL,
          'set_custom': self.BUTTON_LABEL,
          'date_format': self.DATE_FORMAT,
          'start_val': request.GET.get(self.parameter_start, self.INITIAL_START),
          'end_val': request.GET.get(self.parameter_end, self.INITIAL_END),
        }

    @staticmethod
    def to_dtime(text):
        """Convert string to datetime."""
        try:
            return datetime.fromisoformat(text)
        except ValueError:
            return None

    def expected_parameters(self):
        """Parameter list for filter."""
        return [self.parameter_name, self.parameter_start, self.parameter_end]

    def lookups(self, request, _model_admin):
        """Return a list of tuples.

        The first element in each tuple is the coded value for the option that will appear in the URL query.
        The second element is the human-readable name for the option that will appear in the right sidebar.
        """
        return [i[:2] for i in self.options]

    def queryset(self, request, queryset):
        """Return the filtered queryset.

        Based on the value provided in the query string and retrievable via `self.value()`.
        """
        value = self.value()

        if value is None:
            return queryset

        if value == self.option_custom:

            if self.parameter_start in self.used_parameters:
                dtime = self.to_dtime(self.used_parameters[self.parameter_start])
                if dtime:
                    queryset = queryset.filter(**{self.field_path + "__gte": dtime})

            if self.parameter_end in self.used_parameters:
                dtime = self.to_dtime(self.used_parameters[self.parameter_end])
                if dtime:
                    queryset = queryset.filter(**{self.field_path + "__lt": dtime})

            return queryset

        if value == self.option_null:
            return queryset.filter(**{self.field_path + "__isnull": True})

        now = datetime.utcnow()
        delta = self.interval.get(value, self.WRONG_OPTION_VALUE)

        if delta < 0:  # in past
            params = {
              self.field_path + "__gte": now + timedelta(seconds=delta),
              self.field_path + "__lt": now,
            }
        else:  # in future
            params = {
              self.field_path + "__lte": now + timedelta(seconds=delta),
              self.field_path + "__gt": now,
            }

        return queryset.filter(**params)

    def value(self):
        """Return the string provided in the request's query string for this filter.

        None if the value wasn't provided.
        """
        return self.used_parameters.get(self.parameter_name)

    def choices(self, changelist):
        """Define filter shortcuts."""
        yield {
          KEY_SELECTED: self.value() is None,
          KEY_QUERY: changelist.get_query_string(remove=[self.parameter_name]),
          KEY_DISPLAY: self.ALL_LABEL,
        }

        for lookup, title in self.lookup_choices:
            yield {
              KEY_SELECTED: self.value() == str(lookup),
              KEY_QUERY: changelist.get_query_string({self.parameter_name: lookup}),
              KEY_DISPLAY: title,
            }

        if self.is_null_option:
            yield {
              KEY_SELECTED: self.value() == self.option_null,
              KEY_QUERY: changelist.get_query_string({self.parameter_name: self.option_null}),
              KEY_DISPLAY: self.NULL_LABEL,
            }

        yield {
          KEY_SELECTED: self.value() == self.option_custom,
          KEY_QUERY: changelist.get_query_string({self.parameter_name: self.option_custom}),
          KEY_DISPLAY: self.CUSTOM_LABEL,
        }
