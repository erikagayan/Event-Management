from django.db import models
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=100, verbose_name="Event name")
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=250)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
