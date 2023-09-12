from django.shortcuts import redirect, render
from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response
import requests
from .serializers import RaceSerializer


from races.models import Race


@api_view(['GET'])
def update_races(request):
    try:
        response = requests.get('https://www.dnd5eapi.co/api/races/')

        if response.status_code == 200:
            race_data = response.json()
            
            for race in race_data['results']:
                race_object = Race.objects.get_or_create(
                    name=race['name']
                )

            return redirect('characters')
                    
    except Exception as e:
        # Zde byste měli zachytit a zpracovat chyby, například logováním
        print(f"Chyba při aktualizaci dat o rasách: {str(e)}")


@api_view(['GET'])
def get_races(request):
    races = Race.objects.all()

    serializer = RaceSerializer(races, many=True)
    return Response(serializer.data)