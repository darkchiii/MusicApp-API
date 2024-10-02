from django.db import models
from django.conf import settings
from albums.models import Album
import os

def track_upload_path(instance, filename):
    return os.path.join('albums', instance.album.name, filename)

class Track(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='track_owner')
    # genres = models.ManyToManyField('Genre', related_name='track_genres')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(blank=False, max_length=100)
    num_of_plays = models.PositiveBigIntegerField(default=0)
    duration = models.PositiveIntegerField() # Track duration in seconds.
    path = models.FileField(upload_to=track_upload_path, default='')

    def __str__(self):
        return self.title

class Played(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_played')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='played')
    played_date = models.DateTimeField(auto_now_add=True)
    played_counter = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.track.title

class Liked(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_liked')
    track = models.ForeignKey(Track, on_delete=models.CASCADE,  related_name='liked')
    liked_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.track.title
