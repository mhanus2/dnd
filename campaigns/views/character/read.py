from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from campaigns.decorators import campaign_and_player_required
from campaigns.models import (
    Campaign,
    Character,
)
from campaigns.serializers import (
    CharacterSerializer,
    CharactersInCampaignListSerializer,
)


@api_view(["GET"])
def get_characters(request, campaign_id: int):
    campaign = get_object_or_404(Campaign, id=campaign_id)
    characters = Character.objects.filter(campaign=campaign, player=request.user)

    if not characters:
        return Response(
            data={"detail": "No character for this user in this campaign!"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = CharactersInCampaignListSerializer(characters, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@campaign_and_player_required
def get_character_detail(request, character):
    serializer = CharacterSerializer(character)
    return Response(serializer.data)
