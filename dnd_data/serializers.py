from rest_framework import serializers

from django.contrib.auth.models import User

from .models import Race, CharacterClass, Background, Alignment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username'] 

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ['name']

class CharacterClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacterClass
        fields = ['name']

class BackgroundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Background
        fields = ['name']    

class AlignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alignment
        fields = ['name'] 