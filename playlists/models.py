from django.conf import settings
from django.db import models
from tracks.models import Track

class Playlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='playlist_owner')
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300, blank=True)
    date_added = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class TracksInPlaylist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='u')
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='tracks_from_playlist')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='tracks_in_playlist')
    date_added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.track.title