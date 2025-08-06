from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from campaigns.decorators import dungeon_master_required
from campaigns.models import Campaign
from campaigns.serializers import SerializerCampaignCreation, SerializerSessionCreation


@api_view(["POST"])
def create_campaign(request):
    user_instance = request.user

    if not user_instance.groups.filter(name="DM").exists():
        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    data = request.data
    data['dungeon_master_id'] = user_instance.id

    serializer = SerializerCampaignCreation(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@dungeon_master_required
def create_session(request, campaign_id):
    get_object_or_404(Campaign, id=campaign_id)

    data = request.data
    data['campaign'] = campaign_id

    serializer = SerializerSessionCreation(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
