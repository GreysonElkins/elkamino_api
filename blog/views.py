from django.shortcuts import get_object_or_404

from .models import Entry
from api.decorators import json_or_template

@json_or_template('blog/index.html')
def index(request):
    entries = Entry.objects.all().order_by('-pub_date')
    # TODO: order by, clean data
    return entries

@json_or_template('blog/entry.html')
def entry(request, pk):
    result = get_object_or_404(Entry, pk=pk)
    return result
