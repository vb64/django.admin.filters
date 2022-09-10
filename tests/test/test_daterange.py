"""Daterange filter tests.

make test T=test_daterange.py
"""
from datetime import datetime
from django.urls import reverse
from django.contrib.admin import site
from django.test import RequestFactory
from . import TestBase


class TestsDaterange(TestBase):
    """Daterange filter tests.

    https://github.com/django/django/blob/main/tests/admin_filters/tests.py
    """

    request_factory = RequestFactory()

    def setUp(self):
        """Set up Daterange filter tests."""
        super().setUp()
        from django_admin_filters.daterange import DateRange
        from example.models import Log

        self.log = Log(text="text1")
        self.log.save()
        self.url = reverse('admin:example_log_changelist')
        self.field_path = 'timestamp1'
        self.pname = DateRange.parameter_name_mask + self.field_path
        self.queryset = Log.objects.all()

        from django.contrib.auth import get_user_model

        self.admin = get_user_model().objects.create_superuser(
          username='superuser',
          email='mail@example.com',
          password='password'
        )

    @staticmethod
    def test_to_dtime():
        """Method to_dtime."""
        from django_admin_filters.daterange import DateRange

        assert DateRange.to_dtime('xxx') is None
        assert DateRange.to_dtime('2022-09-01 00:00') == datetime(2022, 9, 1)

    def admin_get(self, params):
        """Get request from admin."""
        request = self.request_factory.get(self.url, params)
        request.user = self.admin
        return request

    def test_is_null_option(self):
        """Filter with is_null_option option."""
        from example import admin
        from example.models import Log

        request = self.admin_get({})
        modeladmin = admin.Admin(Log, site)
        changelist = modeladmin.get_changelist_instance(request)

        flt = changelist.get_filters(request)[0][0]

        flt.is_null_option = True
        assert len(list(flt.choices(changelist))) == 5
        flt.is_null_option = False
        assert len(list(flt.choices(changelist))) == 4
