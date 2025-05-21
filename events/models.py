from django.db import models
from django.conf import settings


class Event(models.Model):
    """Model representing an event created by a user (organizer)."""

    title = models.CharField(max_length=100, verbose_name="Event name")
    description = models.TextField(verbose_name="Description")
    date = models.DateTimeField(verbose_name="Event date and time")
    location = models.CharField(max_length=250, verbose_name="Location")
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name = "events",
        verbose_name = "Organizer"
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participated_events",
        verbose_name="Participants",
        blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
