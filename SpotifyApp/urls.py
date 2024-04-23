from django.urls import path 
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ArtistViewSet, GenreViewSet, TrackViewSet, AlbumViewSet, PlaylistViewSet, TracksInPlaylistView, TrackInPlaylistDetailView, PlayedView, LikedView, LikedDetailView, TopArtistsView, TopSongsView

artists_list = ArtistViewSet.as_view({
    'get': 'list', #tylko authenticated
    'post': 'create' #tylko authenticated
})
artists_detail = ArtistViewSet.as_view({
    'get': 'retrieve', #tylko authenticated
    'put': 'update', # authenticated + owner property
    'patch': 'partial_update', # authenticated + owner property
    'delete': 'destroy' # authenticated + owner property
})
albums_list = AlbumViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
albums_detail = AlbumViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
tracks_list = TrackViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
tracks_detail = TrackViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})
playlists_list = PlaylistViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
playlists_detail = PlaylistViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [ #endpoints
    path('artists/', artists_list, name='artists-list'),
    path('artists/<int:pk>/', artists_detail, name='artist-detail'),
    path('albums/', albums_list, name='albums-list'),
    path('albums/<int:pk>/', albums_detail, name='album-detail'),
    path('tracks/', tracks_list, name='tracks-list'),
    path('tracks/<int:pk>/', tracks_detail, name='track-detail'),
    path('playlists/', playlists_list, name='playlists-list'),
    path('playlist/<int:pk>/', playlists_detail, name='playlist-detail'),
    path('playlist/<int:playlist_id>/tracks/', TracksInPlaylistView.as_view(), name='tracks-in-playlists-list'),
    path('playlist/<int:playlist_id>/track/<int:track_id>/', TrackInPlaylistDetailView.as_view(), name='tracks-in-playlist-detail'),
    path('played/<int:user_id>/', PlayedView.as_view(), name='played-tracks'),
    path('liked/<int:user_id>/', LikedView.as_view(), name='liked-tracks'),
    path('liked/<int:user_id>/<int:track_id>/', LikedDetailView.as_view(), name='liked-detail'),
    path('top-artists/<int:user_id>/', TopArtistsView.as_view(), name='top-artist'),
    path('top-songs/<int:user_id>/', TopSongsView.as_view(), name='top-songs'),

]
urlpatterns = format_suffix_patterns(urlpatterns)
