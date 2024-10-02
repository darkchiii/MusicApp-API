from django.shortcuts import render
from rest_framework import viewsets
from .models import Album
from .serializers import AlbumSerializer
from rest_framework.permissions import IsAuthenticated
from Spotify.permissions import IsOwnerOrReadOnly

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
