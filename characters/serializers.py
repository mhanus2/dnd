from rest_framework import serializers

from characters.models import Character

from dnd_data.serializers import UserSerializer, AlignmentSerializer, BackgroundSerializer, CharacterClassSerializer, RaceSerializer


class CharacterSerializer(serializers.ModelSerializer):
    character_class = CharacterClassSerializer()
    race = RaceSerializer()
    background = BackgroundSerializer()
    alignment = AlignmentSerializer()
    player = UserSerializer()
    
    class Meta:
        model = Character
        fields = ['id', 'name', 'level', 'race', 'character_class', 'background', 'alignment', 'player']