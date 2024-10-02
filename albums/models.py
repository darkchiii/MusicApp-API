from django.conf import settings
from django.db import models
# from artists.models import Artist

class Album(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    artists = models.ManyToManyField('artists.Artist', related_name='albums_artists')
    release_date = models.DateField()
    duration = models.PositiveIntegerField(default=0) # Album duration in seconds.
    num_of_tracks = models.PositiveIntegerField(default=0)
    cover = models.ImageField(upload_to='static/album_covers/', blank=True)

    def __str__(self):
        return self.name
