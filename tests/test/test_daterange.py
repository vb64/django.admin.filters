"""Daterange filter tests.

make test T=test_daterange.py
"""
from datetime import datetime
from . import TestBase


class TestsDaterange(TestBase):
    """Daterange filter tests.

    https://github.com/django/django/blob/main/tests/admin_filters/tests.py
    """

    def setUp(self):
        """Set up Daterange filter tests."""
        super().setUp()
        from django_admin_filters import DateRange
        from example.models import Log

        self.log = Log(text="text1")
        self.log.save()
        self.field_path = 'timestamp1'
        self.pname = DateRange.parameter_name_mask + self.field_path

    @staticmethod
    def test_to_dtime():
        """Method to_dtime."""
        from django_admin_filters import DateRange

        assert DateRange.to_dtime('xxx') is None
        assert DateRange.to_dtime('2022-09-01 00:00') == datetime(2022, 9, 1)

    def test_is_null_option(self):
        """Filter with is_null_option option."""
        request = self.admin_get({})
        changelist = self.modeladmin.get_changelist_instance(request)

        flt = changelist.get_filters(request)[0][1]

        flt.is_null_option = True
        assert len(list(flt.choices(changelist))) == 5
        flt.is_null_option = False
        assert len(list(flt.choices(changelist))) == 4

    def test_queryset_null(self):
        """Filter queryset null option."""
        from django_admin_filters import DateRange

        request = self.admin_get({self.pname: DateRange.option_null})
        changelist = self.modeladmin.get_changelist_instance(request)
        flt_null = changelist.get_filters(request)[0][0]
        flt_null.is_null_option = True
        assert flt_null.queryset(request, self.queryset)

    def test_queryset_option(self):
        """Filter queryset shortcut option."""
        from example import admin

        admin.DateRange.options = (
          ('1h', "1 hour", 60 * 60),
        )
        request = self.admin_get({self.pname: '1h'})

        changelist = self.modeladmin.get_changelist_instance(request)
        flt_future = changelist.get_filters(request)[0][1]
        assert not flt_future.queryset(request, self.queryset)

        admin.DateRange.options = (
          ('1h', "-1 hour", -60 * 60),
        )
        changelist = self.modeladmin.get_changelist_instance(request)
        flt_past = changelist.get_filters(request)[0][1]
        assert flt_past.queryset(request, self.queryset) is not None

    def test_queryset_custom(self):
        """Filter queryset custom option."""
        from example import admin

        request = self.admin_get({
          self.pname: admin.Timestamp1Filter.option_custom,
          admin.Timestamp1Filter.parameter_start_mask.format(self.field_path): '2022-01-01 00:00',
          admin.Timestamp1Filter.parameter_end_mask.format(self.field_path): '2022-01-02 00:00',
        })

        changelist = self.modeladmin.get_changelist_instance(request)

        flt_custom = changelist.get_filters(request)[0][1]
        assert not flt_custom.queryset(request, self.queryset)

    def test_queryset_custom_wrong(self):
        """Filter queryset wrong custom option."""
        from example import admin

        request = self.admin_get({
          admin.Timestamp1Filter.parameter_start_mask.format(self.field_path): 'xxx',
          admin.Timestamp1Filter.parameter_end_mask.format(self.field_path): 'xxx',
          self.pname: admin.Timestamp1Filter.option_custom,
        })

        changelist = self.modeladmin.get_changelist_instance(request)
        flt = changelist.get_filters(request)[0][0]
        assert flt.queryset(request, self.queryset)

    def test_queryset_custom_empty(self):
        """Filter queryset empty custom option."""
        from example import admin

        request = self.admin_get({self.pname: admin.DateRange.option_custom})
        changelist = self.modeladmin.get_changelist_instance(request)
        flt = changelist.get_filters(request)[0][0]
        assert flt.queryset(request, self.queryset)
