from django.views import generic
from django.shortcuts import render

from .models import Entry

class IndexView(generic.ListView):
    template_name = "blog/index.html"
    context_object_name = "blog_entries"

    def get_queryset(self):
        return Entry.objects.order_by("-pub_date")

class EntryView(generic.DetailView):
    model = Entry
    template_name = "blog/entry.html"

# Create your views here.
