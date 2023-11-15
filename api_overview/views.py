from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.urls import URLResolver, URLPattern
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
