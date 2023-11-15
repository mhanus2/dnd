from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from campaigns.serializers import (
    SerializerCharacterCreation,
)


@api_view(["POST"])
def create_character(request, campaign_id):
    data = request.data
    data["player"] = request.user.id
    data["campaign"] = campaign_id

    serializer = SerializerCharacterCreation(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


