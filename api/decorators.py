import json
from functools import wraps

from django.core.serializers import serialize
from django.http import HttpResponse
from django.shortcuts import render

def json_or_template(template):
    def decorator(view):
        @wraps(view)
        def _wrapped_view(request, *args, **kwargs):
            output = view(request, *args, **kwargs)
            if request.headers.get('content-type') == 'application/json':
                response = {
                    'data': serialize('json', output),
                    'status': 200
                }
                return HttpResponse(json.dumps(response), content_type="application/json")
            else:
                return render(request, template, { "output": output }) 
        return _wrapped_view
    return decorator
