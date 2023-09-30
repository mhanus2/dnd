from rest_framework import serializers

from characters.serializers import CharacterSerializer
from dnd_data.serializers import UserSerializer

from campaigns.models import Campaign


class CampaignListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'description', 'number_of_characters']

class CampaignSerializer(serializers.ModelSerializer):
    dungeon_master = UserSerializer()
    characters = CharacterSerializer(many=True)
    
    class Meta:
        model = Campaign
        exclude = ('created', )
        
class CampaignTypeSerializer(serializers.Serializer):
    user_is_dm = serializers.BooleanField(default=False)
    dm = CampaignListSerializer(many=True, read_only=True)
    player = CampaignListSerializer(many=True, read_only=True)
