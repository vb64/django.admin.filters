"""Models definition."""
from django.db import models


class Log(models.Model):
    """Log entry with timestamp."""

    text = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=None, null=True)
