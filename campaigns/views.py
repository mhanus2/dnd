from rest_framework.decorators import api_view, permission_classes, action

from rest_framework.response import Response

from .serializers import CampaignTypeSerializer, CampaignSerializer, CharacterSerializer, CharactersInCampaignListSerializer
from campaigns.models import Campaign, Character
from django.http import HttpResponseNotFound
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status

from django.contrib.auth.models import User

from .decorators import dungeon_master_required
import json
from django.http import JsonResponse



#todo - uprava kampane - pridat vsechny fieldy

# Campaign views
@api_view(['GET'])
def get_campaigns(request):
    user_instance = request.user if request.user.is_authenticated else User.objects.get(id=1)

    dm_campaigns = Campaign.objects.filter(dungeon_master=user_instance).distinct()
    player_campaigns = Campaign.objects.filter(~Q(dungeon_master=user_instance)).distinct()

    serializer = CampaignTypeSerializer({
        'user_is_dm': user_instance.groups.filter(name='DM').exists(),
        'dm': dm_campaigns,
        'player': player_campaigns,
    })

    return Response(serializer.data)

@api_view(['GET'])
def get_campaign_detail(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    serializer = CampaignSerializer(campaign)
    return Response(serializer.data)

@api_view(['POST'])
def create_campaign(request):
    if not request.user.groups.filter(name='DM').exists():
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN) 

    user_instance = request.user if request.user.is_authenticated else User.objects.get(id=1)

    data = json.loads(request.body)

    campaign = Campaign.objects.create(
        name=data.get('name'),
        dungeon_master=user_instance,
        description=data.get('description'),
    )

    response_data = {'message': 'Campaign created successfully', 'campaign_id': campaign.id}
    return JsonResponse(response_data, status=201)

@api_view(['PUT'])
@dungeon_master_required
def update_campaign(request, campaign_id):
    data = request.data

    campaign = get_object_or_404(Campaign, id=campaign_id)

    campaign.name = data.get('name', campaign.name)
    campaign.description = data.get('description', campaign.description)

    campaign.save()

    serializer = CampaignSerializer(campaign)

    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@dungeon_master_required
def delete_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    if campaign.dungeon_master != request.user:
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    campaign.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Character views
@api_view(['GET'])
def get_characters(request, campaign_id: int):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    characters = Character.objects.filter(campaign=campaign)

    if not characters:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CharactersInCampaignListSerializer(characters, many=True)
    return Response(serializer.data)
     
@api_view(['GET'])
def get_character_detail(request, campaign_id, character_id):
    user_instance = request.user if request.user.is_authenticated else User.objects.get(id=1)

    character = get_object_or_404(Character, id=character_id, campaign=campaign_id)

    if character.player != user_instance:
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
    
    serializer = CharacterSerializer(character)
    return Response(serializer.data)

@api_view(['POST'])
def create_character(request, campaign_id):
    user_instance = request.user if request.user.is_authenticated else User.objects.get(id=1)

    data = json.loads(request.body)

    character = Character.objects.create(
        name=data.get('name'),
        character_class_id=data.get('character_class'),
        level=data.get('level', 1),
        race_id=data.get('race'),
        background_id=data.get('background'),
        alignment_id=data.get('alignment'),
        player_id=user_instance.id,
        campaign_id=campaign_id 
    )

    response_data = {'message': 'Character created successfully', 'character_id': character.id}
    return JsonResponse(response_data, status=201)

@api_view(['PATCH'])
def update_character(request, character_id):
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
def delete_character(request, character_id):
    user_instance = request.user if request.user.is_authenticated else User.objects.get(id=1)

    character = get_object_or_404(Character, id=character_id)

    if character.player != user_instance:
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    character.status = 'inactive'
    character.save()

    return Response({"detail": "Campaign successfully set inactive."}, status=status.HTTP_204_NO_CONTENT)
