from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response

from .serializers import CampaignSerializer
from campaigns.models import Campaign


@api_view(['GET'])
def get_campaigns(request):
    campaigns = Campaign.objects.all()

    serializer = CampaignSerializer(campaigns, many=True)
    return Response(serializer.data)
     