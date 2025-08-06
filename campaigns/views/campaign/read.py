from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from campaigns.models import Campaign, Character
from campaigns.serializers.campaign import SerializerCampaignType, SerializerCampaign


@api_view(["GET"])
def get_campaigns(request):
    user_instance = request.user

    dm_campaigns = Campaign.objects.filter(dungeon_master=user_instance).distinct()
    player_campaigns = Campaign.objects.filter(
        ~Q(dungeon_master=user_instance)
    ).distinct()

    serializer = SerializerCampaignType(
        {
            "user_is_dm": user_instance.groups.filter(name="DM").exists(),
            "dm": dm_campaigns,
            "player": player_campaigns,
        }
    )

    return Response(serializer.data)


@api_view(["GET"])
def get_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    # Check if the user is the dungeon master or a player in the campaign
    if request.user != campaign.dungeon_master and not Character.objects.filter(campaign=campaign,
                                                                                player=request.user).exists():
        return Response({"detail": "You do not have permission to access this campaign."},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = SerializerCampaign(campaign)
    return Response(serializer.data)
