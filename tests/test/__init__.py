"""Root class for testing."""
from django.test import TestCase, Client, RequestFactory


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

    def login_admin(self):
        """Login as admin."""
        self.client.login(username=self.admin.username, password=self.admin_pass)
