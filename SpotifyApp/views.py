from rest_framework import permissions, status, generics, mixins, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from django.contrib.auth import authenticate, get_user_model # If used custom user model
from .models import Artist, Album, Genre, Track, Playlist, TracksInPlaylist, Played, Liked
from .serializers import ArtistSerializer, GenreSerializer, TrackSerializer, AlbumSerializer, PlaylistSerializer, TracksInPlaylistSerializer, PlayedSerializer, LikedSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta
from collections import Counter

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class ArtistViewSet(viewsets.ModelViewSet): 
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticated]

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False
        serializer = TrackSerializer(data=request.data, many=many, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TracksInPlaylistView(generics.ListCreateAPIView): #list create 
    #obsługa tworzenia nowego obiektu TracksInPlaylist
    serializer_class = TracksInPlaylistSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field_trackid = 'track_id'
    lookup_field_playlistid = 'playlist_id'
   
    def get_queryset(self): #get
        playlist_id = self.kwargs['playlist_id'] #pobierane z url
        return TracksInPlaylist.objects.filter(playlist_id=playlist_id)
   
    def create(self, request, *args, **kwargs): #post pobierane z body
        playlist_id = self.kwargs['playlist_id']
        track_id = request.data.get('track_id')
        user = request.user.id
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(): 
            serializer.save(user_id=user, playlist_id=playlist_id, track_id=track_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TrackInPlaylistDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TracksInPlaylistSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_url_kwarg = 'track_id'
    
    def get_queryset(self):
        playlist_id = self.kwargs['playlist_id'] #pobierane z url
        track_id = self.kwargs[self.lookup_url_kwarg] #pobierane z url
        print(f"Playlist ID: {playlist_id}, track ID: {track_id}")
        return TracksInPlaylist.objects.filter(playlist__id=playlist_id, id=track_id)

class PlayedView(generics.ListCreateAPIView):
    serializer_class = PlayedSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user_id = self.kwargs['user_id']  #user z url
        limit = self.request.query_params.get('limit', None)

        if limit is not None:
            try:
                limit = int(limit)
                return Played.objects.filter(user_id=user_id).order_by('-played_date')[:limit] #-played_date sortowanie od największego rekordu
            except ValueError:
                return Played.objects.filter(user_id=user_id)
        else:
            return Played.objects.filter(user_id=user_id)

    def create(self, request, *args, **kwargs):
        #user z request i track z body
        user = self.request.user.id
        track = request.data.get('track')
        try:
            track = Track.objects.get(pk=track)
        except Track.DoesNotExist:
            raise Http404("Track does not exist")
        track.num_of_plays += 1
        track.save()
        print(f"user: {user}, track ID: {track}")
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(): 
            serializer.save(user_id=user, track=track)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class LikedView(generics.ListCreateAPIView):
    serializer_class = LikedSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self): #LikedView' should either include a `queryset` attribute, or override the `get_queryset()` method.
        user_id = self.kwargs['user_id']
        return Liked.objects.filter(user_id=user_id)
    
    def create(self, request, *args, **kwargs):
        user = self.request.user.id
        track_id = request.data.get('track')
        try:
            liked = Liked.objects.get(track=track_id)
        except Liked.DoesNotExist:
            liked = None
        if liked is not None:
            return Response({"detail": "Object already exists."}, status=status.HTTP_409_CONFLICT)
        try:
            track = Track.objects.get(pk=track_id)
        except Track.DoesNotExist:
            raise Http404("Track does not exist")
        print(f"user: {user}, track ID: {track}")
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(): 
            serializer.save(user_id=user, track=track)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikedDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = LikedSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field_trackid = 'track_id'
    lookup_field_userid = 'user_id'
    def get_object(self):
        user = self.kwargs.get(self.lookup_field_userid)
        track = self.kwargs.get(self.lookup_field_trackid)
        print(f"user: {user}, track ID: {track}")
        print(f"type user: {type(user)}, type track ID: {type(track)}")
        return Liked.objects.get(user=user, track=track)

class TopArtistsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, user_id, format=None):
        today = datetime.now()
        start_date = today - timedelta(days=30)
        plays = Played.objects.filter(user=user_id, played_date__gte=start_date)
        artist_counts = Counter()
        for play in plays:
            for artist in play.track.album.artists.all():
                artist_counts[artist.name] += 1
        top_artists = artist_counts.most_common()
        data = {
            'top artists': top_artists
        }
        return Response(data, status=status.HTTP_200_OK)
    
class TopSongsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, user_id, format=None):
        today = datetime.now()
        start_date = today - timedelta(days=30)
        plays = Played.objects.filter(user=user_id, played_date__gte=start_date) 
        track_counts = Counter()

        for play in plays:
            # for track in play.track: track nie jest iterowalny
            track_counts[play.track.title] += 1
        top_tracks = track_counts.most_common()
        print(top_tracks)
        data={
            "top tracks": top_tracks
        }
        return Response(data, status=status.HTTP_200_OK)

