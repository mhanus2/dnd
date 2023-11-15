from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from campaigns.decorators import dungeon_master_required
from campaigns.models import Campaign
from campaigns.serializers import CampaignUpdateSerializer


@api_view(["PUT"])
@dungeon_master_required
def update_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    data = request.data

    serializer = CampaignUpdateSerializer(campaign, data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
