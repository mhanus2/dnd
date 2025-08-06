from rest_framework import serializers

from campaigns.models import Campaign, Session


class SerializerCampaignUpdate(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ["name", "description"]


class SerializerSessionUpdate(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ["name", "description"]
