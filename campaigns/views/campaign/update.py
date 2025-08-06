from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from campaigns.decorators import dungeon_master_required
from campaigns.models import Campaign, Session
from campaigns.serializers import SerializerCampaignUpdate, SerializerSessionUpdate


@api_view(["PUT"])
@dungeon_master_required
def update_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    data = request.data

    serializer = SerializerCampaignUpdate(campaign, data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
@dungeon_master_required
def update_session(request, campaign_id, session_id):
    session = get_object_or_404(Session, id=session_id)

    data = request.data

    serializer = SerializerSessionUpdate(session, data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
