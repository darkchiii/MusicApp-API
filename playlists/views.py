from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from .serializers import PlaylistSerializer, TracksInPlaylistSerializer
from .models import Playlist, TracksInPlaylist
from tracks.models import Track
from rest_framework.exceptions import ValidationError
from Spotify.permissions import IsAuthenticatedOrReadOnly, IsOwner, IsOwnerOrReadOnly

# Create your views here.
class PlaylistView(viewsets.ModelViewSet):
    serializer_class = PlaylistSerializer
    permission_classes = [IsOwnerOrReadOnly]

# See logged in user playlists
    def get_queryset(self):
        return Playlist.objects.filter(user=self.request.user)

# Create playlist
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# See user playlists
class UserPlaylistView(generics.ListAPIView):
    serializer_class = TracksInPlaylistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = self.request.user

        if user.id == int(user_id):
            playlists = Playlist.objects.filter(user=user)
            return playlists
        else:
            playlists = Playlist.objects.filter(user=user_id, public=True)
            return playlists

# Add track to playlist, if playlist is not specified create new playlist named like track
# List Create Delete
class TracksInPlaylistView(generics.ListCreateAPIView, generics.DestroyAPIView):
    serializer_class = TracksInPlaylistSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        playlist_id = self.kwargs.get('playlist_id')

        if playlist_id:
            return TracksInPlaylist.objects.filter(user=self.request.user, playlist_id=playlist_id).order_by('-date_added')
        else:
            return ValidationError({"detail:": "Playlist id not provided."})

    def perform_create(self, serializer):
        track_id = self.kwargs.get("track_id")
        playlist_id = self.kwargs.get("playlist_id")
        user = self.request.user

        try:
            track = Track.objects.get(id=track_id)
        except Track.DoesNotExist:
            raise ValidationError("Track not found")

        if playlist_id:
            try:
                playlist = Playlist.objects.get(id=playlist_id, user=user)
            except Playlist.DoesNotExist:
                raise ValidationError("Playlist not found.")
        else:
            playlist = Playlist.objects.create(
                user=user,
                name=track.title
            )

        tracks_in_playlist, created = TracksInPlaylist.objects.get_or_create(user=user, playlist=playlist, track=track)
        if not created:
            raise ValidationError({"detail": "Track already exists in the playlist."})

        serializer.save(user=user, playlist=playlist, track=track)

    def destroy(self, request, *args, **kwargs):
        tracks_in_playlist_id = self.kwargs.get('tracks_in_playlist_id')
        # playlist_id = self.kwargs.get('playlist_id')

        try:
            track_in_playlist = TracksInPlaylist.objects.get(id=tracks_in_playlist_id, user=self.request.user)
            print(track_in_playlist)
            track_in_playlist.delete()
            return Response({"message": "Track removed from playlist"}, status=status.HTTP_204_NO_CONTENT)
        except TracksInPlaylist.DoesNotExist:
            return Response({"message": "Track not found in playlist"}, status=status.HTTP_404_NOT_FOUND)
