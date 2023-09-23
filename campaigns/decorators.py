from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from campaigns.models import Campaign
from rest_framework import status


def dungeon_master_required(function):
    def wrap(request, *args, **kwargs):
        campaign_id = kwargs.get('campaign_id')
        campaign = get_object_or_404(Campaign, id=campaign_id)

        if campaign.dungeon_master != request.user:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        return function(request, *args, **kwargs)

    return wrap