from rest_framework import serializers

from campaigns.models import Character


class SerializerCharacterBasicInfo(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ["name", "race", "background", "alignment"]


class SerializerCharacterHealth(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ["max_health", "current_health", "armor_class"]


class SerializerCharacterAttributes(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ["proficiency_bonus", "inspiration", "initiative", "status", "speed"]


class SerializerCharacterMagic(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ["magical_property", "magical_attack_bonus"]


class SerializerCharacterNotes(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = [
            "notes",
        ]
