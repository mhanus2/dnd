import json

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.urls import URLResolver, URLPattern
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from campaigns.urls import urlpatterns


def list_urls(lis, parent_pattern='', acc=None):
    if acc is None:
        acc = []
    if not lis:
        return
    l = lis[0]
    if isinstance(l, URLPattern):
        full_pattern = parent_pattern + str(l.pattern)
        acc.append(full_pattern)
    elif isinstance(l, URLResolver):
        new_parent_pattern = parent_pattern + str(l.pattern)
        list_urls(l.url_patterns, new_parent_pattern, acc)
    list_urls(lis[1:], parent_pattern, acc)
    return acc


@api_view(['GET'])
def get_api_overview(request):
    urls = list_urls(urlpatterns, 'campaigns/')
    return Response(urls)


@api_view(['GET'])
@permission_classes([AllowAny])
def csrf_check(request):
    return JsonResponse({'message': 'CSRF token set'}, status=200)


@csrf_exempt
@require_POST
def custom_login(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
    except (json.JSONDecodeError, KeyError) as e:
        return JsonResponse({'status': 'error', 'message': 'Invalid request data.'}, status=400)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'status': 'success', 'message': 'Logged in successfully.'}, status=200)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid credentials.'}, status=400)
