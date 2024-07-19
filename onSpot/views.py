import os

from django.shortcuts import render, redirect

from .decorators import spotify_authentication

@spotify_authentication()
def index(request):
    
    return render(request, 'onSpot/index.html')

def auth(request):
    client_id = os.getenv('SPOTIFY_ID')
    scope=' '.join([
        'user-read-private', 
        'user-read-email', 
        'playlist-read-private', 
        'playlist-read-collaborative'
    ])
    redirect_uri=os.getenv('BASE_URL') + '/onSpot/'

    return redirect(f'https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}')
