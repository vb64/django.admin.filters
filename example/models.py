"""Models definition."""
from django.db import models


class Log(models.Model):
    """Log entry with timestamp."""

    text = models.CharField(max_length=100)
    timestamp1 = models.DateTimeField(default=None, null=True)
    timestamp2 = models.DateTimeField(default=None, null=True)
