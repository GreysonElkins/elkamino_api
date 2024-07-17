from django.views import generic
from django.shortcuts import get_list_or_404

from .models import Entry
from api.decorators import json_or_template

@json_or_template('blog/index.html')
def index(request):
    entries = get_list_or_404(Entry)
    # TODO: order by, clean data
    return entries

class EntryView(generic.DetailView):
    model = Entry
    template_name = "blog/entry.html"
