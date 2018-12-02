import json

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .models import Task


@require_POST
def set_state(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        pk = int(data['pk'])
        state = int(data['state'])
    except Exception as e:
        return JsonResponse({'error': str(e)} if settings.DEBUG else {}, status=400)

    object = get_object_or_404(Task, pk=pk)
    object.state = state
    object.save()

    return HttpResponse(status=200)
