from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from campaigns.models import Campaign


@api_view(["POST"])
def create_campaign(request):
    if not request.user.groups.filter(name="DM").exists():
        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    user_instance = request.user
    data = request.data

    campaign = Campaign.objects.create(
        name=data.get("name"),
        dungeon_master=user_instance,
        description=data.get("description"),
    )

    return Response(
        {"message": "Campaign created successfully", "campaign_id": campaign.id},
        status=status.HTTP_201_CREATED,
    )
