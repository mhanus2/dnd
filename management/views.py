from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse

from django.shortcuts import redirect, render
from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response
import requests

from dnd_data.models import Race, CharacterClass, Background, Alignment

from django.contrib.auth.decorators import login_required



@login_required
def get_management_tools(request):
    races = Race.objects.all()
    character_classes = CharacterClass.objects.all()
    context = {
        'races': races,
        'character_classes': character_classes
    }

    return render(request, 'management.html', context)


@login_required
def update_races(request):
    existing_races = Race.objects.values_list('name', flat=True)
    new_races_created = []

    try:
        response = requests.get('https://www.dnd5eapi.co/api/races/')
        response.raise_for_status()

        races_data = response.json()['results']
        
        for new_race in races_data:
            if new_race['name'] not in existing_races:
                race_details = fetch_race_details(new_race['index'])

                if race_details:
                    new_race_created = Race.objects.create(
                        name=new_race['name'],
                        speed=race_details['speed']
                    )
                    new_races_created.append(new_race_created)
                else:
                    continue
        
        if new_races_created:
            created_objects_json = [obj.to_json() for obj in new_races_created]
            return JsonResponse({'created_objects': created_objects_json}, status=201)
        return JsonResponse({}, status=204)
                    
    except requests.exceptions.RequestException as e:
        return Response({'message': f'Failed to fetch races data: {str(e)}'}, status=500)
    
def fetch_race_details(race_index):
    try:
        response = requests.get(f'https://www.dnd5eapi.co/api/races/{race_index}')
        response.raise_for_status()  # Raise an exception for non-200 status codes

        race_data = response.json()
        return race_data

    except requests.exceptions.RequestException:
        return None
    
@login_required
def update_character_classes(request):
    existing_character_classes = CharacterClass.objects.values_list('name', flat=True)
    new_character_classes_created = []

    try:
        response = requests.get('https://www.dnd5eapi.co/api/classes/')
        response.raise_for_status()

        character_classes_data = response.json()['results']
        
        for new_character_class in character_classes_data:
            if new_character_class['name'] not in existing_character_classes:

                new_character_class = CharacterClass.objects.create(
                        name=new_character_class['name'],
                    )
                new_character_classes_created.append(new_character_class)
        
        if new_character_classes_created:
            created_objects_json = [obj.to_json() for obj in new_character_classes_created]
            return JsonResponse({'created_objects': created_objects_json}, status=201)
        return JsonResponse({}, status=204)
                    
    except requests.exceptions.RequestException as e:
        return Response({'message': f'Failed to fetch races data: {str(e)}'}, status=500)
    

@login_required
def update_backgrounds(request):
    existing_backgrounds = Background.objects.values_list('name', flat=True)
    fetch_new_data('backgrounds', existing_backgrounds, Background)

@login_required
def update_alignments(request):
    existing_alignments = Alignment.objects.values_list('name', flat=True)
    fetch_new_data('alignments', existing_alignments, Alignment)
    
def fetch_new_data(api_endpoint, existing_data, model):
    try:
        response = requests.get(f'https://www.dnd5eapi.co/api/{api_endpoint}')
        response.raise_for_status()


        fetched_data = response.json()['results']
        
        for new_data in fetched_data:

            if new_data['name'] not in existing_data:
                print(new_data['name'])
                model.objects.create(
                        name=new_data['name'],
                    )
        
        return JsonResponse({'message': 'success'}, status=201)
                    
    except requests.exceptions.RequestException as e:
        return Response({'message': f'Failed to fetch {api_endpoint} data: {str(e)}'}, status=500)
    