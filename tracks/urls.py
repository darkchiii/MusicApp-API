from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrackViewSet, PlayTrackView, LikeTrackView, SearchView

router = DefaultRouter()
router.register(r'tracks', TrackViewSet, basename='track')

urlpatterns = [
    path('', include(router.urls)),
    path('play/<int:track_id>/', PlayTrackView.as_view(), name='play-track'),
    path('played/', PlayTrackView.as_view(), name='user-most-played-tracks'),
    path('liked/', LikeTrackView.as_view(), name='user-liked-tracks'),
    path('like/<int:track_id>/', LikeTrackView.as_view(), name='destroy-like-track'),
    path('search/', SearchView.as_view(), name='search'),

]
