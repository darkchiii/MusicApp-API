# from django.db import models
# from django.conf import settings
# import os

# # class Artist(models.Model):
# #     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='artist_owner', default='', null=True)
# #     name = models.CharField(blank=False, max_length=50)
# #     bio = models.TextField(blank = False)
# #     albums = models.ManyToManyField('Album', related_name='artists_albums', blank=True)
# #     listeners_counter = models.PositiveBigIntegerField(default=0)
# #     def __str__(self):
# #         return self.name

# # class Album(models.Model):
# #     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='album_owner', default='', null=True)
# #     name = models.CharField(blank=False, max_length=50)
# #     artists = models.ManyToManyField('Artist', related_name='albums_artists', blank=True)
# #     release_date = models.DateField(blank=False)
# #     duration = models.DecimalField(blank=False, max_digits=4, decimal_places=2, default=0) #automatyczne liczenie gdzieś
# #     num_of_tracks = models.PositiveIntegerField(blank=False, default=0)
# #     cover = models.ImageField(upload_to='album_covers/', blank=True, null=True)
# #     def __str__(self):
# #         return self.name

# # class Genre(models.Model):
# #     name = models.CharField(blank=False, max_length=30)
# #     def __str__(self):
# #         return self.name

# # def track_upload_path(instance, filename):
# #     return os.path.join('albums', instance.album.name, filename)

# # class Track(models.Model):
# #     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='track_owner', default='', null=True)
# #     genres = models.ManyToManyField('Genre', related_name='track_genres')
# #     album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='album_with_track')
# #     title = models.CharField( blank=False, max_length=50)
# #     num_of_plays = models.PositiveBigIntegerField(default=0)
# #     duration = models.DecimalField(blank=False, max_digits=4, decimal_places=2)
# #     path = models.FileField(upload_to=track_upload_path, default='')
# #     def __str__(self):
# #         return self.title

# class Playlist(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_playlist', default='')
#     name = models.CharField(blank=False, max_length=50)
#     description = models.CharField(blank=True, max_length=300)
#     date_added = models.DateTimeField(blank=False, auto_now=True)
#     def __str__(self):
#         return self.name

# class TracksInPlaylist(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_tracks_in_playlist', default='',blank=True,null=True)
#     playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='tracks_from_playlist', default='' )
#     track = models.ManyToManyField('Track', related_name='playlist_tracks')
#     date_added = models.DateTimeField(blank=False, auto_now=True)
#     def __str__(self):
#         first_track = self.track.first()
#         if first_track:
#             return first_track.title
#         else:
#             return 'No tracks in playlist'

