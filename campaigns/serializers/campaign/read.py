from rest_framework import serializers

from campaigns.models import (
    Campaign,
    Character,
    Session
)
from dnd_data.serializers import UserSerializer


class CampaignCharactersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('name',)


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['name', 'date']


class CampaignSerializer(serializers.ModelSerializer):
    dungeon_master = UserSerializer()
    characters = CampaignCharactersSerializer(many=True, read_only=True)
    sessions = SessionSerializer(many=True, read_only=True)

    class Meta:
        model = Campaign
        fields = ["name", "description", "dungeon_master", "characters", "sessions"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        characters = Character.objects.filter(campaign=instance)
        character_serializer = CampaignCharactersSerializer(characters, many=True)
        ret["characters"] = character_serializer.data

        sessions = Session.objects.filter(campaign=instance)
        session_serializer = SessionSerializer(sessions, many=True)
        ret["sessions"] = session_serializer.data

        return ret


class CampaignListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ["id", "name", "description"]


class CampaignTypeSerializer(serializers.Serializer):
    user_is_dm = serializers.BooleanField(default=False)
    dm = CampaignListSerializer(many=True, read_only=True)
    player = CampaignListSerializer(many=True, read_only=True)
