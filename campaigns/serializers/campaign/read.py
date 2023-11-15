from rest_framework import serializers

from campaigns.models import (
    Campaign,
    Character,
    Session
)
from dnd_data.serializers import SerializerUser


class SerializerCampaignCharacters(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ('name',)


class SerializerSession(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['name', 'description', 'date', 'character_count']


class SerializerCampaign(serializers.ModelSerializer):
    dungeon_master = SerializerUser()
    characters = SerializerCampaignCharacters(many=True, read_only=True)
    sessions = SerializerSession(many=True, read_only=True)

    class Meta:
        model = Campaign
        fields = ["name", "description", "dungeon_master", "characters", "sessions"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        characters = Character.objects.filter(campaign=instance)
        character_serializer = SerializerCampaignCharacters(characters, many=True)
        ret["characters"] = character_serializer.data

        sessions = Session.objects.filter(campaign=instance)
        session_serializer = SerializerSession(sessions, many=True)
        ret["sessions"] = session_serializer.data

        return ret


class SerializerCampaignList(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ["id", "name", "description"]


class SerializerCampaignType(serializers.Serializer):
    user_is_dm = serializers.BooleanField(default=False)
    dm = SerializerCampaignList(many=True, read_only=True)
    player = SerializerCampaignList(many=True, read_only=True)
