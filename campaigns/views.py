from rest_framework.decorators import api_view, permission_classes, action

from rest_framework.response import Response

from .serializers import CampaignTypeSerializer, CampaignSerializer
from campaigns.models import Campaign, Character
from django.http import HttpResponseNotFound

from django.shortcuts import get_object_or_404
from rest_framework import status

from django.contrib.auth.models import User

from .decorators import dungeon_master_required


@api_view(['GET'])
def get_campaigns(request):
    user_instance = request.user if request.user.is_authenticated else User.objects.get(id=1)

    characters = Character.objects.filter(player=user_instance)

    dm_campaigns = Campaign.objects.filter(dungeon_master=user_instance)
    player_campaigns = Campaign.objects.filter(characters__in=characters)

    serializer = CampaignTypeSerializer({
        'dm': dm_campaigns,
        'player': player_campaigns
    })

    return Response(serializer.data)


@api_view(['GET'])
def get_campaign_detail(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    if campaign.dungeon_master != request.user and request.user not in campaign.characters.all():
        return HttpResponseNotFound()

    serializer = CampaignSerializer(campaign)
    return Response(serializer.data)


@api_view(['POST'])
@dungeon_master_required
def update_campaign_detail(request, campaign_id):
    data = request.data

    campaign = get_object_or_404(Campaign, id=campaign_id)

    campaign.name = data.get('name', campaign.name)
    campaign.description = data.get('description', campaign.description)

    campaign.save()

    serializer = CampaignSerializer(campaign)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@dungeon_master_required
def delete_campaign_detail(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    if campaign.dungeon_master != request.user:
        return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

    campaign.delete()
    return Response({"detail": "Campaign successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
