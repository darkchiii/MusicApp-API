from rest_framework import serializers
from .models import Playlist, TracksInPlaylist
from tracks.serializers import TrackSerializer

class TracksInPlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = TracksInPlaylist
        fields = ['id', 'user', 'playlist', 'track', 'date_added']
        read_only_fields = ['id', 'user', 'playlist', 'track', 'date_added']


class PlaylistSerializer(serializers.ModelSerializer):
    tracks_from_playlist = TracksInPlaylistSerializer(many=True)

    class Meta:
        model = Playlist
        fields = ['id', 'user', 'name', 'description', 'public', 'date_added', 'tracks_from_playlist']
        read_only_fields = ['id', 'user', 'date_added', 'tracks_from_playlist']
