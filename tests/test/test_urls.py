"""Test urls.

make test T=test_urls.py
"""
from django.urls import reverse
from . import TestBase


class TestsUrls(TestBase):
    """Url tests.

    https://docs.djangoproject.com/en/3.2/ref/contrib/admin/#admin-reverse-urls
    """

    def test_home(self):
        """Root page."""
        response = self.client.get(reverse('home'))
        assert response.status_code == 200

    def test_admin_views(self):
        """Admin view pages."""
        self.login_admin()

        response = self.client.get(reverse('admin:example_log_changelist'))
        assert response.status_code == 200

        response = self.client.get(reverse('admin:example_log_add'))
        assert response.status_code == 200
