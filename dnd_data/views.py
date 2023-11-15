from rest_framework.decorators import api_view

from rest_framework.response import Response
from .serializers import SerializerRace

from .models import Race


@api_view(['GET'])
def get_races(request):
    races = Race.objects.all()

    serializer = SerializerRace(races, many=True)
    return Response(serializer.data)