"""Models definition."""
from django.db import models

STATUS_CHOICES = (
  ('P', 'Pending'),
  ('A', 'Approved'),
  ('R', 'Rejected'),
)

NUM_CHOICES = (
  (0, 'Zero'),
  (1, 'One'),
  (2, 'Two'),
)


class Log(models.Model):
    """Log entry with timestamp."""

    text = models.CharField(max_length=100)
    timestamp1 = models.DateTimeField(default=None, null=True)
    timestamp2 = models.DateTimeField(default=None, null=True)
    status = models.CharField(max_length=1, default='P', choices=STATUS_CHOICES)
    number = models.IntegerField(default=0, choices=NUM_CHOICES)
    is_online = models.BooleanField(default=False)
    is_trouble1 = models.BooleanField(default=False)
    is_trouble2 = models.BooleanField(default=False)

    @property
    def color(self):
        """Color for object state."""
        status = 'red'
        if self.is_online:
            status = 'green'
            if self.is_trouble1 or self.is_trouble2:
                status = 'yellow'

        return status
