from django.db import models
from django.conf import settings
from django.utils import timezone

class Event(models.Model):
    organizer   = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events'
    )
    title       = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    location    = models.CharField(max_length=200)
    start_date  = models.DateTimeField()
    end_date    = models.DateTimeField()
    banner      = models.ImageField(upload_to='event_banners/', blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return self.start_date >= timezone.now()

    @property
    def going_count(self):
        return self.rsvps.filter(status=RSVP.Status.GOING).count()

    @property
    def interested_count(self):
        return self.rsvps.filter(status=RSVP.Status.INTERESTED).count()


class RSVP(models.Model):

    class Status(models.TextChoices):
        GOING      = 'going',      'Going'
        INTERESTED = 'interested', 'Interested'

    user  = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rsvps'
    )
    event  = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    status = models.CharField(max_length=12, choices=Status.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')  # one RSVP per user per event

    def __str__(self):
        return f'{self.user.email} — {self.event.title} ({self.status})'