from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from campaigns.decorators import dungeon_master_required
from campaigns.models import Campaign


@api_view(["DELETE"])
@dungeon_master_required
def delete_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    campaign.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
