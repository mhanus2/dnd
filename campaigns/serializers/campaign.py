from rest_framework import serializers

from campaigns.models import (
    Campaign,
    Character,
)
from dnd_data.serializers import UserSerializer
from .character import CharacterSerializer


class CampaignListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ["id", "name", "description"]


class CampaignSerializer(serializers.ModelSerializer):
    dungeon_master = UserSerializer()
    characters = CharacterSerializer(many=True, read_only=True)

    class Meta:
        model = Campaign
        exclude = ("created",)

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        characters = Character.objects.filter(campaign=instance)
        character_serializer = CharacterSerializer(characters, many=True)
        ret["character"] = character_serializer.data

        return ret


class CampaignTypeSerializer(serializers.Serializer):
    user_is_dm = serializers.BooleanField(default=False)
    dm = CampaignListSerializer(many=True, read_only=True)
    player = CampaignListSerializer(many=True, read_only=True)
