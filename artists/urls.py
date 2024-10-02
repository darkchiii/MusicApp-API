from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArtistViewSet, FavoriteUserArtists, FavoriteArtists

router = DefaultRouter()
router.register(r'artists', ArtistViewSet, basename='artist')

urlpatterns = [
    path('', include(router.urls)),
    path('favorite/', FavoriteUserArtists.as_view(), name='user-fav-artists'),
    path('all_favorite/', FavoriteArtists.as_view(), name='all-fav-artists')
]