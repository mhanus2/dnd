from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Race, CharacterClass, Background, Alignment


class SerializerUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class SerializerRace(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ['name']


class SerializerCharacterClass(serializers.ModelSerializer):
    class Meta:
        model = CharacterClass
        fields = ['name']


class SerializerBackground(serializers.ModelSerializer):
    class Meta:
        model = Background
        fields = ['name']


class SerializerAlignment(serializers.ModelSerializer):
    class Meta:
        model = Alignment
        fields = ['name']
