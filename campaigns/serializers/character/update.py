from rest_framework import serializers

from campaigns.models import (
    Character,
)


class CharacterBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ["name", "race"]
