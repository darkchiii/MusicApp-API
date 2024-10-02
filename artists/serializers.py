from rest_framework import serializers
from django.contrib.auth import get_user_model # If used custom user model
from .models import Artist
from django.core.exceptions import ObjectDoesNotExist

class ArtistSerializer(serializers.ModelSerializer):
# ModelSerializer automatycznie obsługuje tworzenie, odczytywanie, aktualizację i usuwanie danych dla modelu Artist.
    class Meta:
        model = Artist
        fields = ['id', 'user', 'name', 'bio', 'listeners_counter']
        read_only_fields = ['id', 'user', 'listeners_counter']

class FavoriteArtistSerializer(serializers.Serializer):
    artist_name = serializers. CharField(source='track__album__artists__name')
    total_plays = serializers.IntegerField()

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['artist_name'] = instance.get('artists__name', 'Unknown artist')

    #     return representation