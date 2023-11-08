from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from campaigns.models import Campaign
from campaigns.serializers.campaign import CampaignTypeSerializer, CampaignSerializer


@api_view(["GET"])
def get_campaigns(request):
    user_instance = request.user

    dm_campaigns = Campaign.objects.filter(dungeon_master=user_instance).distinct()
    player_campaigns = Campaign.objects.filter(
        ~Q(dungeon_master=user_instance)
    ).distinct()

    serializer = CampaignTypeSerializer(
        {
            "user_is_dm": user_instance.groups.filter(name="DM").exists(),
            "dm": dm_campaigns,
            "player": player_campaigns,
        }
    )

    return Response(serializer.data)


@api_view(["GET"])
def get_campaign_detail(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    serializer = CampaignSerializer(campaign)
    return Response(serializer.data)
