import os
import json
import base64
import requests
from functools import wraps

from django.shortcuts import redirect

def spotify_authentication():
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            code = request.GET.get('code')
            if not request.session.get('spotify_token', False):
                if code == None: return redirect('/onSpot/auth')
                else: get_bearer_token(request, code)
            if not request.session.get('user'): get_user(request)
            return view(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def get_bearer_token(request, code):
    credential =  os.getenv("SPOTIFY_ID") + ':' + os.getenv("SPOTIFY_SECRET")
    credential_bytes = credential.encode("utf-8")
    redirect_uri = os.getenv('BASE_URL') + '/onSpot/'
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
    
    request.session['spotify_token'] = data.get('access_token')

def get_user(request):
    res = requests.get(
        'https://api.spotify.com/v1/me', 
        headers={ 'Authorization': 'Bearer ' + request.session.get('spotify_token', '') })
    request.session['user'] = json.loads(res.content)
