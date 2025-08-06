from django.contrib.auth.models import User
from rest_framework import serializers

from campaigns.models import Campaign, Session
from dnd_data.serializers import SerializerUser


class SerializerCampaignCreation(serializers.ModelSerializer):
    dungeon_master = SerializerUser(read_only=True)
    dungeon_master_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='dungeon_master'
    )

    class Meta:
        model = Campaign
        fields = ["name", "description", "dungeon_master", "dungeon_master_id"]


class SerializerSessionCreation(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ["name", "description", "date", "campaign"]
