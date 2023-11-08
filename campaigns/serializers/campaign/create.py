from rest_framework import serializers

from campaigns.models import Campaign


class CampaignCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ["name", "description", "dungeon_master"]
