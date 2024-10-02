from django.shortcuts import render
from django.db.models import Sum
from rest_framework import viewsets, generics
from .models import Artist
from tracks.models import Played
from .serializers import ArtistSerializer, FavoriteArtistSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from Spotify.permissions import IsOwner, IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly

class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [IsOwnerOrReadOnly]

# Add artist to database.
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Get user top artists view.
class FavoriteUserArtists(generics.ListAPIView):
    serializer_class = FavoriteArtistSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        favourite_artists = Played.objects.filter(user=self.request.user) \
            .values('track__album__artists__name') \
            .annotate(total_plays=Sum('played_counter')) \
            .order_by('-total_plays')
        return favourite_artists

# Get top artists.
class FavoriteArtists(generics.ListAPIView):
    serializer_class = FavoriteArtistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        now = timezone.now()
        last_28_days = now-timedelta(days=28)

        favourite_artists = Played.objects.values('track__album__artists__name') \
            .annotate(total_plays=Sum('played_counter')) \
            .order_by('-total_plays').filter(played_date__gte=last_28_days)
        return favourite_artists

