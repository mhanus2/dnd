from django.shortcuts import redirect, render
from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response
import json
from django.contrib.auth.models  import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import status

from .serializers import CharacterSerializer, CampaignListSerializer
from characters.models import Character
from campaigns.models import Campaign


@api_view(['GET'])
def get_characters(request):
    user_instance = request.user if request.user.is_authenticated else User.objects.get(id=1)

    characters = Character.objects.filter(player=user_instance)

    serializer = CampaignListSerializer(characters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_campaign_characters(request, campaign_id: int):
    user_instance = request.user if request.user.is_authenticated else User.objects.get(id=1)

    campaign = get_object_or_404(Campaign, id=campaign_id)

    characters = campaign.characters.filter(player=user_instance)

    if not characters:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CampaignListSerializer(characters, many=True)
    return Response(serializer.data)
     
@api_view(['GET'])
def get_character_detail(request, character_id):
    user_instance = request.user if request.user.is_authenticated else User.objects.get(id=1)

    character = get_object_or_404(Character, id=character_id)

    if character.player != user_instance:
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CharacterSerializer(character)
    return Response(serializer.data)

@api_view(['POST'])
def create_character(request):
    user_instance = request.user if request.user.is_authenticated else User.objects.get(id=1)

    data = json.loads(request.body)

    character = Character.objects.create(
        name=data.get('name'),
        character_class_id=data.get('character_class'),
        level=data.get('level', 1),
        race_id=data.get('race'),
        background_id=data.get('background'),
        alignment_id=data.get('alignment'),
        player_id=user_instance.id
    )

    response_data = {'message': 'Character created successfully', 'character_id': character.id}
    return JsonResponse(response_data, status=201)

@api_view(['PATCH'])
def update_character_detail(request, character_id):
    user_instance = request.user if request.user.is_authenticated else User.objects.get(id=1)

    character = get_object_or_404(Character, id=character_id)

    if character.player != user_instance:
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    data = request.data

    character.name = data.get('name', character.name)

    character.save()

    serializer = CharacterSerializer(character)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH'])
def delete_character_detail(request, character_id):
    user_instance = request.user if request.user.is_authenticated else User.objects.get(id=1)

    character = get_object_or_404(Character, id=character_id)

    if character.player != user_instance:
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    character.status = 'inactive'
    character.save()

    return Response({"detail": "Campaign successfully set inactive."}, status=status.HTTP_204_NO_CONTENT)
    