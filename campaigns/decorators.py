from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from campaigns.models import Campaign, Character


def dungeon_master_required(function):
    def wrap(request, *args, **kwargs):
        campaign_id = kwargs.get('campaign_id')
        campaign = get_object_or_404(Campaign, id=campaign_id)

        if campaign.dungeon_master != request.user:
            return Response({"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)

        return function(request, *args, **kwargs)

    return wrap


def campaign_and_player_required(function):
    def wrap(request, **kwargs):
        campaign_id = kwargs.get('campaign_id')
        character_id = kwargs.get('character_id')
        character = get_object_or_404(Character, id=character_id)

        if campaign_id != character.campaign.id:
            return Response(
                {"detail": "Character does not belong to this campaign."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.user != character.player:
            return Response(
                {"detail": "Permission denied."},
                status=status.HTTP_403_FORBIDDEN
            )

        return function(request, character)

    return wrap
