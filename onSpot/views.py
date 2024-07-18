import os
import json
import base64
import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse

def index(request):
    code = request.GET.get('code')
    error= request.GET.get('error')
    if not code and not error:
        return redirect('/onSpot/auth')
    elif not error:
        credential =  os.getenv("SPOTIFY_ID") + ':' + os.getenv("SPOTIFY_SECRET")
        credential_bytes = credential.encode("utf-8")
        redirect_uri=os.getenv('BASE_URL') + '/onSpot/'

        res = requests.post(
            'https://accounts.spotify.com/api/token', 
            headers={
                'content-type': 'application/x-www-form-urlencoded', 
                'Authorization': f'Basic {base64.b64encode(credential_bytes).decode("utf-8")}'
            },
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': redirect_uri
            }
        )

        data = json.loads(res.content)
        token = data.get('access_token')
        user = requests.get('https://api.spotify.com/v1/me', headers={ 'Authorization': 'Bearer ' + token })
        user_id = json.loads(user.content).get('id')
        print(user_id)
    return render(request, 'onSpot/index.html')

def get_access_token(request):
    client_id = os.getenv('SPOTIFY_ID')
    scope=' '.join([
        'user-read-private', 
        'user-read-email', 
        'playlist-read-private', 
        'playlist-read-collaborative'
    ])
    redirect_uri=os.getenv('BASE_URL') + '/onSpot/'

    return redirect(f'https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&scope={scope}&redirect_uri={redirect_uri}')
