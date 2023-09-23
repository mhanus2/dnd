from rest_framework.decorators import api_view

from rest_framework.response import Response
from .serializers import RaceSerializer

from .models import Race


@api_view(['GET'])
def get_races(request):
    races = Race.objects.all()

    serializer = RaceSerializer(races, many=True)
    return Response(serializer.data)