from rest_framework.decorators import api_view, permission_classes, action

from rest_framework.response import Response

from .serializers import CampaignTypeSerializer, CampaignSerializer
from campaigns.models import Campaign, Character
from django.http import HttpResponseNotFound

from django.shortcuts import get_object_or_404
from rest_framework import status

from django.contrib.auth.models import User

from .decorators import dungeon_master_required
import json
from django.http import JsonResponse



#todo - uprava kampane - pridat vsechny fieldy


@api_view(['GET'])
def get_campaigns(request):
    user_instance = request.user if request.user.is_authenticated else User.objects.get(id=1)

    characters = Character.objects.filter(player=user_instance)

    dm_campaigns = Campaign.objects.filter(dungeon_master=user_instance).distinct()
    player_campaigns = Campaign.objects.filter(characters__in=characters).distinct()

    serializer = CampaignTypeSerializer({
        'user_is_dm': user_instance.groups.filter(name='Doctor').exists(),
        'dm': dm_campaigns,
        'player': player_campaigns,
    })

    return Response(serializer.data)


@api_view(['GET'])
def get_campaign_detail(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    if campaign.dungeon_master != request.user and request.user.id not in campaign.characters.values_list('player', flat=True):
        return HttpResponseNotFound()

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

    campaign.characters.set(data.get('characters'))
    campaign.save()

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
    return Response({"detail": "Campaign successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
