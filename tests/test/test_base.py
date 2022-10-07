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
