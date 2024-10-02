from rest_framework import serializers
from .models import Track, Played, Liked

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'user', 'album', 'title', 'num_of_plays', 'duration']
        read_only_fields = ['id', 'user', 'num_of_plays']

    def create(self, validated_data):
        return Track.objects.create(**validated_data)

class TrackListSerializer(serializers.ListSerializer):
    child = TrackSerializer()

    def create(self, validated_data):
        tracks = [Track(**item) for item in validated_data]
        return Track.objects.bulk_create(tracks)

class PlayedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Played
        fields = ['id', 'user', 'track', 'played_date', 'played_counter']
        read_only_fields = ['id', 'user', 'track', 'played_date']

class TrackPlayedSummarySerializer(serializers.Serializer):
    track__title = serializers.CharField()
    total_played = serializers.IntegerField()

class LikedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liked
        fields = ['id', 'user', 'track', 'liked_date']
        read_only_fields = ['id', 'user', 'track']