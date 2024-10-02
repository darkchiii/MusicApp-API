from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import path, include
from rest_framework import routers, serializers, viewsets
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('docs/', include_docs_urls(title='My little API')),
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('', include('artists.urls')),
    path('', include('albums.urls')),
    path('', include('tracks.urls')),
    path('', include('playlists.urls')),
]
