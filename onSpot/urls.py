from django.urls import path

from . import views

app_name='onSpot'
urlpatterns=[
    path('', views.index, name='index'),
    path('auth', views.get_access_token, name='auth')
]
