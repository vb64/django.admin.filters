"""Multi choice filter tests.

make test T=test_multi_choice.py
"""
from . import TestBase


class TestsMultiChoice(TestBase):
    """MultiChoice filter tests."""

    def setUp(self):
        """Set up MultiChoice filter tests."""
        super().setUp()

        from django_admin_filters import MultiChoice
        self.field_path = 'status'
        self.pname = MultiChoice.parameter_name_mask + self.field_path

    def test_queryset(self):
        """Filter queryset with checkbox set."""
        from example.models import STATUS_CHOICES

        request = self.admin_get({
          self.pname: STATUS_CHOICES[0][0],
        })

        changelist = self.modeladmin.get_changelist_instance(request)

        flt_choice = changelist.get_filters(request)[0][0]
        assert flt_choice.queryset(request, self.queryset) is not None

    def test_queryset_ext(self):
        """Filter queryset with MultiChoiceExt."""
        from example.admin import ColorFilter

        pname = ColorFilter.parameter_name
        request = self.admin_get({pname: 'green' + ColorFilter.CHOICES_SEPARATOR + 'red'})

        changelist = self.modeladmin.get_changelist_instance(request)
        flt_color = changelist.get_filters(request)[0][4]
        assert flt_color.queryset(request, self.queryset) is not None
