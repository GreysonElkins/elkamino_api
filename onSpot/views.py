import os
import json
import requests

from django.shortcuts import render, redirect

from .spotify import Spotify

def index(request):
    playlists = Spotify(request).get(
        'https://api.spotify.com/v1/me/playlists'
    )
    return render(request, 'onSpot/index.html', {'data': playlists})

def auth(request):
    client_id = os.getenv('SPOTIFY_ID')
    scope=' '.join([
        'user-read-private', 
        'user-read-email', 
        'playlist-read-private',
        'user-library-read', 
        'playlist-read-collaborative'
    ])
    redirect_uri=os.getenv('BASE_URL') + '/onSpot/'

    return redirect(f'https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}')

# @spotify_authentication()
def playlists(request, playlist_id):
    # playlist = spotify(request, requests.get, f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks')
    playlist = Spotify(request).get(f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks')    
    return render(request, 'onSpot/playlists.html', {'playlist': playlist})

# @spotify_authentication()
def liked_songs(request):
    Spotify(request).get(
        request,
        request.get,
        'https://api.spotify.com/v1/me/tracks'
    )
