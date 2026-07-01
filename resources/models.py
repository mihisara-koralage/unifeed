from django.db import models
from django.conf import settings
import re

class Resource(models.Model):

    class Category(models.TextChoices):
        NOTES      = 'notes',      'Notes'
        PAST_PAPERS = 'past_papers', 'Past Papers'
        TUTORIALS  = 'tutorials',  'Tutorials'
        BOOKS      = 'books',      'Books'
        TOOLS      = 'tools',      'Tools & Software'
        OTHER      = 'other',      'Other'

    title       = models.CharField(max_length=200)
    url         = models.URLField(max_length=500)
    category    = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER
    )
    description = models.TextField(max_length=500, blank=True)
    contributor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='resources'
    )
    is_approved = models.BooleanField(default=True)  # admin can hide bad links
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} ({self.get_category_display()})'