import requests

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'onSpot/index.html')

def get_access_token(request):
    headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
    body = {
        'grant_type': 'client-credential',
        'client_id': 'client',
        'client_secret': 'secret'
    }
    res = requests.post('https://accounts.spotify.com/api/token', data=body, headers=headers)
    return HttpResponse(res)
