from django.shortcuts import redirect, render
from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response
import requests

from .serializers import CharacterSerializer
from characters.models import Character


@api_view(['GET'])
def get_characters(request):
    characters = Character.objects.all()

    serializer = CharacterSerializer(characters, many=True)
    return Response(serializer.data)
     
@api_view(['GET'])
def get_character(request, character_id):
    character = Character.objects.get(id=character_id)    
    
    serializer = CharacterSerializer(character)
    return Response(serializer.data)
     