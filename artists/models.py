from django.db import models
from django.conf import settings
from tracks.models import Played, Track
import os
from django.utils import timezone
from datetime import timedelta

class Artist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='artist_owner')
    name = models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    listeners_counter = models.PositiveBigIntegerField(default=0)

    def update_listeners_counter(self):
        now = timezone.now()
        last_28_days = now - timedelta(days=28)
        tracks = Track.objects.filter(album__artists=self)

        unique_listeners = Played.objects.filter(track__in=tracks,
                                                 played_date__gte=last_28_days,
                                                 ).values('user').distinct().count()

        self.listeners_counter = unique_listeners
        self.save()

    def __str__(self):
        return self.name
