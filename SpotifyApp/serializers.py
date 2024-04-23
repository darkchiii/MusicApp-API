from rest_framework import serializers
from django.contrib.auth import get_user_model # If used custom user model
from .models import Artist, Album, Genre, Track, Playlist, Played, Liked, TracksInPlaylist
from django.core.exceptions import ObjectDoesNotExist

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']

class ArtistSerializer(serializers.ModelSerializer):
# ModelSerializer automatycznie obsługuje tworzenie, odczytywanie, aktualizację i usuwanie danych dla modelu Artist.
    albums = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name') #po to zeby wyswietlalo sie po polu name nie id
    class Meta:
        model = Artist
        fields = ['id', 'user', 'name', 'bio', 'albums', 'listeners_counter'] # czy dawać id?

class AlbumSerializer(serializers.ModelSerializer):
    artists = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Artist.objects.all())
    class Meta:
        model = Album
        fields = ['id', 'user', 'name', 'artists', 'release_date', 'duration', 'num_of_tracks', 'cover']
    def create(self, validated_data):
        artist_names = validated_data.pop('artists')
        album = Album.objects.create(**validated_data)
        for artist_name in artist_names:
            artist, _ = Artist.objects.get_or_create(name=artist_name)
            album.artists.add(artist)
            artist.albums.add(album)
        return album

class TrackSerializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Genre.objects.all())
    album = serializers.SlugRelatedField(slug_field='name', queryset=Album.objects.all())
    class Meta:
        model = Track
        fields = ['user', 'id', 'genres', 'album', 'title', 'num_of_plays', 'duration', 'path']
    def create(self, validated_data):
        album_name = validated_data.pop('album')
        genres_data = validated_data.pop('genres')
        album, created = Album.objects.get_or_create(name=album_name)
        track=Track.objects.create(album=album, **validated_data)
        for genre_name in genres_data:
            genre, _ = Genre.objects.get_or_create(name=genre_name)
            track.genres.add(genre)
        return track
    
class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'user', 'name', 'description', 'date_added']

class TracksInPlaylistSerializer(serializers.ModelSerializer): #tworzenie nowego obiektu TracksInPlaylist
    #pola tylko dla metody post ids pobierane z body
    playlist_id = serializers.IntegerField(write_only=True) 
    track_id = serializers.IntegerField(write_only=True)
    playlist = serializers.PrimaryKeyRelatedField(read_only=True)
    track = serializers.SerializerMethodField()  #obliczane na podstawie metody get_track()
    class Meta:
        model = TracksInPlaylist
        fields = ['id', 'user', 'playlist', 'track', 'date_added', 'playlist_id', 'track_id']
        read_only_fields = ['id', 'user', 'date_added']
        
    def get_track(self, obj):
        first_track = obj.track.first()
        return first_track.id if first_track else None  #id tracku, zawartość tracku pochodzi z pola many to many

    def create(self, validated_data):
        playlist_id = validated_data.pop('playlist_id')
        track_id = validated_data.pop('track_id')
        user = self.context['request'].user.id
        #jeśli nie ma playlisty to jest tworzona nowa i nazywa się jak tytuł pierwszego dodanego tracka
        track = Track.objects.get(pk=track_id)
        try:
            playlist = Playlist.objects.get(pk=playlist_id, user_id=user) 
        except ObjectDoesNotExist:
            playlist = Playlist.objects.create(pk=playlist_id, user_id=user, name=track.title)
        trackinplaylist = TracksInPlaylist.objects.create(playlist=playlist, **validated_data)
        trackinplaylist.track.set([track])
        return trackinplaylist

class PlayedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Played
        fields = ['id', 'user', 'track']

class LikedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liked
        fields = ['id', 'user', 'track', 'liked_date']

