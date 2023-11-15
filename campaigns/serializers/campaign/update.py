from rest_framework import serializers

from campaigns.models import Campaign


class SerializerCampaignUpdate(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ["name", "description"]
