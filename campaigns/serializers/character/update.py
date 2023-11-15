from rest_framework import serializers

from campaigns.models import Character


class CharacterBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ["name", "race", "background", "alignment"]


class CharacterHealthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ["max_health", "current_health", "armor_class"]


class CharacterAttributesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ["proficiency_bonus", "inspiration", "initiative", "status", "speed"]


class CharacterMagicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ["magical_property", "magical_attack_bonus"]


class CharacterNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = [
            "notes",
        ]
