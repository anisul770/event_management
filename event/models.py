from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    """Represents an event category (e.g., Conference, Workshop)."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    """Main event model linking to Category and Participants."""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    time = models.TimeField()
    img = models.ImageField(upload_to='event_asset',blank=True,null=True)
    location = models.CharField(max_length=200, blank=True)
    participants = models.ManyToManyField(User,related_name="events", blank=True,default='event_asset/default.jpg')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name} ({self.date})"

    @property
    def is_upcoming(self):
        """Check if event is in the future."""
        return self.date >= timezone.now().date()

    @property
    def participant_count(self):
        """Returns number of participants for this event."""
        return self.participants.count()

