from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlaylistView, UserPlaylistView, TracksInPlaylistView

router = DefaultRouter()
router.register(r'playlist', PlaylistView, basename='playlist')

urlpatterns = [
    path('', include(router.urls)),
    path('playlists/<int:user_id>/', UserPlaylistView.as_view(), name='user-playlist'),
    path('add-track/<int:track_id>/', TracksInPlaylistView.as_view(), name='add-track'),
    path('add-track/<int:track_id>/<int:playlist_id>/', TracksInPlaylistView.as_view(), name='add-track-playlist'),
    path('playlist/<int:playlist_id>/', TracksInPlaylistView.as_view(), name='tracks-in-playists'),
    path('remove-track/<int:tracks_in_playlist_id>/', TracksInPlaylistView.as_view(), name='remove-track-playlist'),
]