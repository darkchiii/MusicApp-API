from rest_framework import serializers
from .models import Album
from tracks.serializers import TrackSerializer

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)

    class Meta:
        model = Album
        fields = ['id', 'user', 'name', 'artists', 'release_date', 'duration', 'num_of_tracks', 'tracks', 'cover']
        read_only_fields = ['id', 'user']