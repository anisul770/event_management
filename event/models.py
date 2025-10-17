from django.db import models
from django.utils import timezone


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
    location = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="events"
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


class Participant(models.Model):
    """Represents an individual attending one or more events."""
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    events = models.ManyToManyField(Event,related_name="participants", blank=True)

    def __str__(self):
        return self.name

    @property
    def total_events(self):
        """Returns number of events the participant is attending."""
        return self.events.count()
