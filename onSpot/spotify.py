import os
import json
import base64
import requests
from functools import wraps

from django.shortcuts import redirect, render
from django.http import HttpResponse

class Spotify:
    def __init__(self, request):
        # will this be a copy or point at the mutable request obj?
        self.request = request

    @property
    def _bearer_token(self):
        return self.request.session.get('spotify_bearer_token', None)

    @property
    def _refresh_token(self):
        return self.request.session.get('spotify_refresh_token', None)

    @property
    def is_authenticated(self):
        return self._bearer_token
    
    def _authenticate(self):
        req = self.request
        code = req.GET.get('code')
        if not self.is_authenticated or code:
            if code == None:
                return redirect('/onSpot/auth')
            elif code: self._get_bearer_token()

    def _get_bearer_token(self):
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
                'code': self.request.GET.get('code', ''),
                'redirect_uri': redirect_uri
            }
        )
        data = json.loads(res.content)
    
        self.request.session['spotify_bearer_token'] = data.get('access_token')
        self.request.session['spotify_refresh_token'] = data.get('refresh_token')

    def _authorize_headers(self, headers = {}, **_):
        headers['Authorization'] = 'Bearer ' + self._bearer_token
        return headers 

    def _refresh_auth(self):
        if not self.refresh_token: raise Exception('no refresh token available')
        res = requests.post(
            'https://accounts.spotify.com/api/token',
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token,
                'client_id': os.getenv("SPOTIFY_ID")
            }
        )

        data = json.loads(res.content)
        del self.request.session['spotify_bearer_token']
        del self.request.session['spotify_refresh_token']
        self.request.session['spotify_bearer_token'] = data.get('access_token')
        self.request.session['spotify_refresh_token'] = data.get('refresh_token')

    def _spotify_api_method(func):
        def inner(self, *args, **kwargs):
            headers = self._authorize_headers()
            try: 
                if not self.is_authenticated: 
                    redirection = self._authenticate()
                    if redirection is not None: return redirection
                res = func(self, *args, headers=headers, **kwargs)
                return json.loads(res.content)
            except Exception as e:
                if '401' in e.args[0]:
                    print(f'Catch this language: {e.args[0]}')
                return HttpResponse(e.args[0])
        return inner
        
    @_spotify_api_method
    def get(self, *args, **kwargs):
        return requests.get(*args, **kwargs)
        
    @_spotify_api_method
    def post(self, *args, **kwargs):
        return requests.post(*args, **kwargs)
