from rest_framework.decorators import api_view

from rest_framework.response import Response

from .serializers import (
    CampaignTypeSerializer,
    CampaignSerializer,
    CharacterSerializer,
    CharactersInCampaignListSerializer,
)
from campaigns.models import Campaign, Character, CharacterAbility, CharacterSkill, SavingThrow
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status

from dnd_data.models import Skill

from django.contrib.auth.models import User

from .decorators import dungeon_master_required
import json


# todo - uprava kampane - pridat vsechny fieldy
MODIFIER_MAP = {
    (1,): -5,
    (2, 3): -4,
    (4, 5): -3,
    (6, 7): -2,
    (8, 9): -1,
    (10, 11): 0,
    (12, 13): 1,
    (14, 15): 2,
    (16, 17): 3,
    (18, 19): 4,
    (20, 21): 5,
    (22, 23): 6,
    (24, 25): 7,
    (26, 27): 8,
    (28, 29): 9,
    (30,): 10,
}

# Campaign views
@api_view(["GET"])
def get_campaigns(request):
    user_instance = (
        request.user if request.user.is_authenticated else User.objects.get(id=1)
    )

    dm_campaigns = Campaign.objects.filter(dungeon_master=user_instance).distinct()
    player_campaigns = Campaign.objects.filter(
        ~Q(dungeon_master=user_instance)
    ).distinct()

    serializer = CampaignTypeSerializer(
        {
            "user_is_dm": user_instance.groups.filter(name="DM").exists(),
            "dm": dm_campaigns,
            "player": player_campaigns,
        }
    )

    return Response(serializer.data)


@api_view(["GET"])
def get_campaign_detail(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    serializer = CampaignSerializer(campaign)
    return Response(serializer.data)


@api_view(["POST"])
def create_campaign(request):
    if not request.user.groups.filter(name="DM").exists():
        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    user_instance = (
        request.user if request.user.is_authenticated else User.objects.get(id=1)
    )

    data = json.loads(request.body)

    campaign = Campaign.objects.create(
        name=data.get("name"),
        dungeon_master=user_instance,
        description=data.get("description"),
    )

    return Response(
        {"message": "Campaign created successfully", "campaign_id": campaign.id},
        status=status.HTTP_201_CREATED,
    )


@api_view(["PUT"])
@dungeon_master_required
def update_campaign(request, campaign_id):
    data = request.data

    campaign = get_object_or_404(Campaign, id=campaign_id)

    campaign.name = data.get("name", campaign.name)
    campaign.description = data.get("description", campaign.description)

    campaign.save()

    serializer = CampaignSerializer(campaign)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
@dungeon_master_required
def delete_campaign(request, campaign_id):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    if campaign.dungeon_master != request.user:
        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    campaign.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# Character views
@api_view(["GET"])
def get_characters(request, campaign_id: int):
    campaign = get_object_or_404(Campaign, id=campaign_id)

    characters = Character.objects.filter(campaign=campaign)

    if not characters:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CharactersInCampaignListSerializer(characters, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_character_detail(request, campaign_id, character_id):
    user_instance = (
        request.user if request.user.is_authenticated else User.objects.get(id=1)
    )

    character = get_object_or_404(Character, id=character_id, campaign=campaign_id)

    if character.player != user_instance:
        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    serializer = CharacterSerializer(character)
    return Response(serializer.data)


@api_view(["POST"])
def create_character(request, campaign_id):
    user_instance = (
        request.user if request.user.is_authenticated else User.objects.get(id=1)
    )

    data = json.loads(request.body)

    character = Character.objects.create(
        name=data.get("name"),
        character_class_id=data.get("character_class"),
        level=data.get("level", 1),
        race_id=data.get("race"),
        background_id=data.get("background"),
        alignment_id=data.get("alignment"),
        player_id=user_instance.id,
        campaign_id=campaign_id,
    )

    return Response(
        {"message": "Character created successfully", "character_id": character.id},
        status=status.HTTP_201_CREATED,
    )


@api_view(["PATCH"])
def update_character(request, character_id):
    user_instance = (
        request.user if request.user.is_authenticated else User.objects.get(id=1)
    )

    character = get_object_or_404(Character, id=character_id)

    if character.player != user_instance:
        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    data = request.data

    character.name = data.get("name", character.name)

    character.save()

    serializer = CharacterSerializer(character)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
def delete_character(request, character_id):
    user_instance = (
        request.user if request.user.is_authenticated else User.objects.get(id=1)
    )

    character = get_object_or_404(Character, id=character_id)

    if character.player != user_instance:
        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    character.status = "inactive"
    character.save()

    return Response(
        {"detail": "Campaign successfully set inactive."},
        status=status.HTTP_204_NO_CONTENT,
    )


@api_view(["PATCH"])
def update_character_abilities(request, campaign_id, character_id):
    character = Character.objects.get(id=character_id, player=request.user)
    character_abilities = CharacterAbility.objects.filter(character=character)

    for character_ability in character_abilities:
        for score_range, modifier_value in MODIFIER_MAP.items():
            if character_ability.score in score_range:
                character_ability.modifier = modifier_value
                break
        character_ability.save()

    return Response(
        {"detail": "Character abilities updated."},
        status=status.HTTP_200_OK,
    )

@api_view(["PATCH"])
def update_character_skills(request, campaign_id, character_id):
    character = get_object_or_404(Character, id=character_id, player=request.user)
    character_abilities = CharacterAbility.objects.filter(character=character)

    for character_ability in character_abilities:
        modifier = character_ability.modifier

        skills = Skill.objects.filter(ability=character_ability.ability)

        for skill in skills:
            character_skill = CharacterSkill.objects.get(
                character=character, skill=skill
            )

            new_value = modifier + character.proficiency_bonus if character_skill.proficiency else modifier

            character_skill.value = new_value
            character_skill.save()

    return Response(
        {"detail": "Character skills updated."},
        status=status.HTTP_200_OK,
    )

@api_view(["PATCH"])
def update_saving_throws(request, campaign_id, character_id):
    character = get_object_or_404(Character, id=character_id, player=request.user)
    saving_throws = SavingThrow.objects.filter(character=character)

    for saving_throw in saving_throws:
        character_ability = CharacterAbility.objects.get(character=character, ability=saving_throw.ability)

        modifier = character_ability.modifier
        new_value = modifier + character.proficiency_bonus if saving_throw.proficiency else modifier

        saving_throw.value = new_value
        saving_throw.save()

    return Response(
        {"detail": "Saving throws updated."},
        status=status.HTTP_200_OK,
    )
