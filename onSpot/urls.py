from django.urls import path

from . import views

app_name='onSpot'
urlpatterns=[
    path('', views.index, name='index'),
    path('auth', views.auth, name='auth'),
    path('playlists/<str:playlist_id>/', views.playlists, name="playlists")
]
