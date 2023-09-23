from django.shortcuts import redirect, render
from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response

from django.contrib.auth.models  import User

from django.shortcuts import get_object_or_404

from .serializers import CharacterSerializer
from characters.models import Character


@api_view(['GET'])
def get_characters(request):
    characters = Character.objects.all()

    serializer = CharacterSerializer(characters, many=True)
    return Response(serializer.data)
     
@api_view(['GET'])
def get_character_detail(request, character_id):
    user_instance = request.user if request.user.is_authenticated else User.objects.get(id=1)

    character = get_object_or_404(Character, id=character_id, player=user_instance)
    
    serializer = CharacterSerializer(character)
    return Response(serializer.data)
     