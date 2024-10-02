# from rest_framework import permissions, status, generics, mixins, viewsets
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from rest_framework.decorators import authentication_classes, permission_classes
# from django.contrib.auth import authenticate, get_user_model # If used custom user model
# from .models import Artist, Album, Genre, Track, Playlist, TracksInPlaylist, Played, Liked
# from .serializers import ArtistSerializer, GenreSerializer, TrackSerializer, AlbumSerializer, PlaylistSerializer, TracksInPlaylistSerializer, PlayedSerializer, LikedSerializer
# from django.shortcuts import get_object_or_404
# from django.http import Http404
# from django.core.exceptions import ObjectDoesNotExist
# from datetime import datetime, timedelta
# from collections import Counter

# class IsOwnerOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return obj.user == request.user


# class GenreViewSet(viewsets.ModelViewSet):
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer
#     permission_classes = [permissions.IsAuthenticated]


