"""Root class for testing."""
from django.test import TestCase, Client, RequestFactory
from django.contrib.admin import site
from django.urls import reverse


class TestBase(TestCase):
    """Base class for tests."""

    request_factory = RequestFactory()

    def setUp(self):
        """Set up Django client."""
        super().setUp()
        self.client = Client()
        self.admin_pass = 'password'

        from django.contrib.auth import get_user_model

        self.admin = get_user_model().objects.create_superuser(
          username='superuser',
          email='mail@example.com',
          password=self.admin_pass
        )

        from example.admin import Admin
        from example.models import Log

        self.modeladmin = Admin(Log, site)
        self.url = reverse('admin:example_log_changelist')
        self.queryset = Log.objects.all()

    def admin_get(self, params):
        """Get request from admin."""
        request = self.request_factory.get(self.url, params)
        request.user = self.admin
        return request

    def login_admin(self):
        """Login as admin."""
        self.client.login(username=self.admin.username, password=self.admin_pass)
