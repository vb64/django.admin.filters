"""Base filter tests.

make test T=test_base.py
"""
import pytest
from . import TestBase


class TestsBaseFilter(TestBase):
    """BaseFilter filter tests."""

    def test_choices(self):
        """Check 'choices' method."""
        from django_admin_filters.base import Filter

        with pytest.raises(NotImplementedError) as err:
            Filter.choices(None, None)
        assert 'choices' in str(err.value)

    def test_lookups(self):
        """Check 'lookups' method."""
        from django_admin_filters.base import FilterSimple

        with pytest.raises(NotImplementedError) as err:
            FilterSimple.lookups(None, None, None)
        assert 'lookups' in str(err.value)

    def test_queryset(self):
        """Check 'queryset' method."""
        from django_admin_filters.base import FilterSimple

        with pytest.raises(NotImplementedError) as err:
            FilterSimple.queryset(None, None, None)
        assert 'queryset' in str(err.value)
