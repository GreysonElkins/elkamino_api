from django.urls import path

from . import views

app_name="blog"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/", views.EntryView.as_view(), name="entry")
]
