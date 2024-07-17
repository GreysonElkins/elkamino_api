from django.http import HttpResponse
from django.core.serializers import serialize
from django.views import generic
from django.shortcuts import render, get_list_or_404

from .models import Entry
from api.decorators import json_or_template

@json_or_template('blog/index.html')
def index(request):
    entries = get_list_or_404(Entry)
    return entries

class IndexView(generic.ListView):
    template_name = "blog/index.html"
    context_object_name = "blog_entries"

    def get_queryset(self):
        return Entry.objects.order_by("-pub_date")

class EntryView(generic.DetailView):
    model = Entry
    template_name = "blog/entry.html"
