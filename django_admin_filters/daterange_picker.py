"""Django admin daterange filter with js widget and shortcuts."""
from django.conf import settings

from .daterange import DateRange


class DateRangePicker(DateRange):
    """Date range filter with js datetime picker widget."""

    template = 'daterange_picker.html'

    INITIAL_START = 'now'
    INITIAL_END = 'now'

    WIDGET_LOCALE = settings.LANGUAGE_CODE
    WIDGET_BUTTON_LABEL = "Set"
    WIDGET_WITH_TIME = True

    WIDGET_START_TITLE = 'Start date'
    WIDGET_START_TOP = -350
    WIDGET_START_LEFT = -400 if WIDGET_WITH_TIME else -100

    WIDGET_END_TITLE = 'End date'
    WIDGET_END_TOP = -350
    WIDGET_END_LEFT = -400 if WIDGET_WITH_TIME else -100

    def __init__(self, field, request, params, model, model_admin, field_path):
        """Apply js widget settings."""
        super().__init__(field, request, params, model, model_admin, field_path)

        self.title['widget_locale'] = self.WIDGET_LOCALE
        self.title['widget_button_label'] = self.WIDGET_BUTTON_LABEL
        self.title['widget_with_time'] = 'true' if self.WIDGET_WITH_TIME else 'false'

        self.title['widget_start_title'] = self.WIDGET_START_TITLE
        self.title['widget_start_top'] = self.WIDGET_START_TOP
        self.title['widget_start_left'] = self.WIDGET_START_LEFT

        self.title['widget_end_title'] = self.WIDGET_END_TITLE
        self.title['widget_end_top'] = self.WIDGET_END_TOP
        self.title['widget_end_left'] = self.WIDGET_END_LEFT
