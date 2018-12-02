import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .models import Schedule


@login_required
@require_POST
def set_participant(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        pk = int(data['pk'])
        action = str(data['action'])
    except Exception as e:
        return JsonResponse({'error': str(e)} if settings.DEBUG else {}, status=400)

    object = get_object_or_404(Schedule, pk=pk)
    if action == 'add':
        object.participants.add(request.user)
    elif action == 'remove':
        object.participants.remove(request.user)
    else:
        return JsonResponse({}, status=400)

    return JsonResponse({}, status=200)
