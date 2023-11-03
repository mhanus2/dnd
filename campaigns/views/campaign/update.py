from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from campaigns.decorators import dungeon_master_required
from campaigns.models import Campaign
from campaigns.serializers import CampaignSerializer


# todo - uprava kampane - pridat vsechny fieldy


@api_view(["PUT"])
@dungeon_master_required
def update_campaign(request, campaign_id):
    data = request.data

    campaign = get_object_or_404(Campaign, id=campaign_id)

    campaign.name = data.get("name", campaign.name)
    campaign.description = data.get("description", campaign.description)

    campaign.save()

    serializer = CampaignSerializer(campaign)

    return Response(serializer.data, status=status.HTTP_200_OK)
