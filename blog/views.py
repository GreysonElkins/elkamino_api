from django.http import HttpResponse
from django.core.serializers import serialize
from django.views import generic
from django.shortcuts import render, get_object_or_404, get_list_or_404

from .models import Entry

def index(request):
    #TODO: clean up JSON - try `django.forms.models.model_to_dict`, may have to abandon `get_list_or_404?`
    entries = get_list_or_404(Entry)
    print(request.headers['content-type'])
    if request.headers['content-type'] == 'application/json':
        response_data = {}
        response_data['data'] = serialize('json', entries)
        response_data['status'] = 200
        return HttpResponse(dumps(response_data), content_type="application/json")
    else:
        return render(request, "blog/index.html", { "blog_entries": entries }) 

class IndexView(generic.ListView):
    template_name = "blog/index.html"
    context_object_name = "blog_entries"

    def get_queryset(self):
        return Entry.objects.order_by("-pub_date")

class EntryView(generic.DetailView):
    model = Entry
    template_name = "blog/entry.html"
