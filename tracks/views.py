from django.shortcuts import render
from rest_framework import viewsets, generics, permissions, serializers, status, filters
from rest_framework.response import Response
from django.db.models import Sum
from .models import Track, Played, Liked
from .serializers import TrackSerializer, TrackListSerializer, PlayedSerializer, LikedSerializer, TrackPlayedSummarySerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from Spotify.permissions import IsOwnerOrReadOnly
from django.utils import timezone
from datetime import timedelta

class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many']=True
        return super().get_serializer(*args, **kwargs)

# Add tracks to database.
    def perform_create(self, serializer):
        tracks = serializer.save(user=self.request.user)

        if isinstance(tracks, list):
            album = tracks[0].album
        else:
            album = tracks.album
        self.update_album_fields(album)

    def update_album_fields(self, album):
        tracks = album.tracks.all()
        album.duration = sum(track.duration for track in tracks)
        album.num_of_tracks = tracks.count()
        album.save()

# Update track instance.
    def perform_update(self, serializer):
        track = serializer.save(user=self.request.user)
        self.update_album_fields(track.album)

# Delete track instance.
    def perform_destroy(self, instance):
        album = instance.album
        instance.delete()
        self.update_album_fields(album)

@method_decorator(csrf_exempt, name='dispatch')
class PlayTrackView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PlayedSerializer
        elif self.request.method == "GET":
            return TrackPlayedSummarySerializer
        return super().get_serializer_class()

# Play track.
    def perform_create(self, serializer):
        print("performing request...")

        track_id = self.kwargs['track_id']
        try:
            track = Track.objects.get(id=track_id)
        except Track.DoesNotExist:
            raise serializers.ValidationError(f"Track with id {track_id} does not exist.")
        # print(f"track:  {track_id}")

        played_instance = serializer.save(user=self.request.user, track=track)
        print(f"Updated played instance {played_instance}")
        played_instance.played_counter = 1
        # print(f"Updated played counter {played_instance.played_counter}")
        played_instance.track.num_of_plays += 1
        played_instance.save()
        played_instance.track.save()

# Get most played tracks from last 28 days.
    def get_queryset(self):
        limit = self.request.query_params.get('limit', None)
        now = timezone.now()
        last_28_days = now-timedelta(days=28)

        played = Played.objects.filter(user=self.request.user, played_date__gte=last_28_days).select_related('track').values(
        'track__title').annotate(total_played=Sum('played_counter')).order_by('-total_played')

        if limit is not None:
            try:
                limit = int(limit)
                return played[:limit]
            except ValueError:
                return played
        else:
            return played

class LikeTrackView(generics.ListCreateAPIView, generics.DestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = LikedSerializer

# Get user liked tracks.
    def get_queryset(self):
        return Liked.objects.filter(user=self.request.user).order_by('-liked_date')

# Like track.
    def perform_create(self, serializer):
        track_id = self.kwargs.get('track_id')
        user = self.request.user

        if Liked.objects.filter(track_id = track_id, user=user).exists():
            raise serializers.ValidationError("You have already liked this track!")

        serializer.save(user=user, track_id=track_id)

# Unlike track.
    def destroy(self, request, *args, **kwargs):
        track_id = self.kwargs.get('track_id')
        user = self.request.user
        like = Liked.objects.get(track_id = track_id, user=user)

        if like:
            like.delete()
            return Response({"message": "Like deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Like not found"}, status=status.HTTP_404_NOT_FOUND)

# Search phrase
class SearchView(generics.ListAPIView):
    search_fields = ['album__name', 'title', 'album__artists__name']
    filter_backends = (filters.SearchFilter,)

    queryset = Track.objects.all()
    serializer_class = TrackSerializer
