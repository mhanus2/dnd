from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from campaigns.serializers import (
    CampaignTypeSerializer,
    CampaignSerializer,
    CharacterSerializer,
    CharactersInCampaignListSerializer,
    CharacterCreationSerializer,
    CharacterAbilitySerializer,
    CharacterSkillSerializer,
    PassiveSkillSerializer,
    SavingThrowSerializer,
    HitDiceSerializer,
    SpellSlotSerializer,
    CharacterBasicInfoSerializer,
    CharacterMultiClassSerializer,
)
from campaigns.models import (
    Campaign,
    Character,
    CharacterAbility,
    CharacterSkill,
    SavingThrow,
    PassiveSkill,
    HitDice,
    SpellSlot,
    CharacterMultiClass,
)
from campaigns.constants import MODIFIER_MAP, PASSIVE_SKILLS
from campaigns.decorators import dungeon_master_required

from dnd_data.models import Skill, Ability, Dice, CharacterClass


# todo - uprava kampane - pridat vsechny fieldy


# Campaign views
@api_view(["GET"])
def get_campaigns(request):
    user_instance = request.user

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

    data = request.data

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
    characters = Character.objects.filter(campaign=campaign, player=request.user)

    if not characters:
        return Response(
            data={"detail": "No characters for this user in this campaign!"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = CharactersInCampaignListSerializer(characters, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_character_detail(request, campaign_id, character_id):
    character = get_object_or_404(Character, id=character_id, campaign=campaign_id)

    if character.player != request.user:
        return Response(
            data={"detail": "Permission denied."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer = CharacterSerializer(character)
    return Response(serializer.data)


# ---------------------------
# Character data manipulation
# ---------------------------
@api_view(["POST"])
def create_character(request, campaign_id):
    data = request.data
    data["player"] = request.user.id
    data["campaign"] = campaign_id

    serializer = CharacterCreationSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
def update_basic_info(request, campaign_id, character_id):
    user_instance = request.user
    character = get_object_or_404(Character, id=character_id)

    if character.player != user_instance:
        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    data = request.data
    data["character"] = character_id

    serializer = CharacterBasicInfoSerializer(character, data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
def update_character_multiclass(request, campaign_id, character_id):
    user_instance = request.user
    character = get_object_or_404(Character, id=character_id)

    if character.player != user_instance:
        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    data = request.data

    response_data = []

    for item in data:
        character_class_instance = CharacterClass.objects.get(id=item["id"])
        item["character"] = character_id

        existing_instance = CharacterMultiClass.objects.get_or_create(
            character=character, character_class=character_class_instance
        )[0]

        serializer = CharacterMultiClassSerializer(existing_instance, data=item)

        if serializer.is_valid():
            serializer.save()
            response_data.append(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(["PATCH"])
def update_character_abilities(request, campaign_id, character_id):
    user_instance = request.user
    character = get_object_or_404(Character, id=character_id)

    if character.player != user_instance:
        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    data = request.data

    response_data = []

    for item in data:
        ability_instance = Ability.objects.get(id=item["ability"])
        item["character"] = character_id

        existing_instance = CharacterAbility.objects.get_or_create(
            character=character, ability=ability_instance
        )[0]

        serializer = CharacterAbilitySerializer(existing_instance, data=item)

        if serializer.is_valid():
            serializer.save()
            response_data.append(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(["PATCH"])
def update_character_skills(request, campaign_id, character_id):
    user_instance = request.user
    character = get_object_or_404(Character, id=character_id)

    if character.player != user_instance:
        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    data = request.data

    response_data = []

    for item in data:
        skill_instance = Skill.objects.get(id=item["skill"])
        item["character"] = character_id

        existing_instance = CharacterSkill.objects.get_or_create(
            character=character, skill=skill_instance
        )[0]

        serializer = CharacterSkillSerializer(existing_instance, data=item)

        if serializer.is_valid():
            serializer.save()
            response_data.append(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(["PATCH"])
def update_passive_skills(request, campaign_id, character_id):
    user_instance = request.user
    character = get_object_or_404(Character, id=character_id)

    if character.player != user_instance:
        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    data = request.data

    response_data = []

    for item in data:
        skill_instance = Skill.objects.get(id=item["skill"])

        if skill_instance.name not in PASSIVE_SKILLS:
            return Response(
                {"message": f"{skill_instance.name} is not passive ability!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        item["character"] = character_id

        existing_instance = PassiveSkill.objects.get_or_create(
            character=character, skill=skill_instance
        )[0]

        serializer = PassiveSkillSerializer(existing_instance, data=item)

        if serializer.is_valid():
            serializer.save()
            response_data.append(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(["PATCH"])
def update_saving_throws(request, campaign_id, character_id):
    user_instance = request.user
    character = get_object_or_404(Character, id=character_id)

    if character.player != user_instance:
        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    data = request.data

    response_data = []

    for item in data:
        ability_instance = Ability.objects.get(id=item["ability"])

        item["character"] = character_id

        existing_instance = SavingThrow.objects.get_or_create(
            character=character, ability=ability_instance
        )[0]

        serializer = SavingThrowSerializer(existing_instance, data=item)

        if serializer.is_valid():
            serializer.save()
            response_data.append(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(["PATCH"])
def update_hit_dices(request, campaign_id, character_id):
    user_instance = request.user
    character = get_object_or_404(Character, id=character_id)

    if character.player != user_instance:
        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    data = request.data

    response_data = []

    for item in data:
        dice_instance = Dice.objects.get(id=item["dice"])

        item["character"] = character_id

        existing_instance = HitDice.objects.get_or_create(
            character=character, dice=dice_instance
        )[0]

        serializer = HitDiceSerializer(existing_instance, data=item)

        if serializer.is_valid():
            serializer.save()
            response_data.append(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(response_data, status=status.HTTP_201_CREATED)


@api_view(["PATCH"])
def update_spell_slots(request, campaign_id, character_id):
    user_instance = request.user
    character = get_object_or_404(Character, id=character_id)

    if character.player != user_instance:
        return Response(
            {"detail": "Permission denied."}, status=status.HTTP_403_FORBIDDEN
        )

    data = request.data

    response_data = []

    for item in data:
        item["character"] = character_id

        existing_instance = SpellSlot.objects.get_or_create(
            character=character, level=item["level"]
        )[0]

        serializer = SpellSlotSerializer(existing_instance, data=item)

        if serializer.is_valid():
            serializer.save()
            response_data.append(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(response_data, status=status.HTTP_201_CREATED)


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
def auto_update_character_abilities(request, campaign_id, character_id):
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
def auto_update_character_skills(request, campaign_id, character_id):
    character = get_object_or_404(Character, id=character_id, player=request.user)
    character_abilities = CharacterAbility.objects.filter(character=character)

    for character_ability in character_abilities:
        modifier = character_ability.modifier

        skills = Skill.objects.filter(ability=character_ability.ability)

        for skill in skills:
            character_skill = CharacterSkill.objects.get(
                character=character, skill=skill
            )

            new_value = (
                modifier + character.proficiency_bonus
                if character_skill.proficiency
                else modifier
            )

            character_skill.value = new_value
            character_skill.save()

    return Response(
        {"detail": "Character skills updated."},
        status=status.HTTP_200_OK,
    )


@api_view(["PATCH"])
def auto_update_saving_throws(request, campaign_id, character_id):
    character = get_object_or_404(Character, id=character_id, player=request.user)
    saving_throws = SavingThrow.objects.filter(character=character)

    for saving_throw in saving_throws:
        character_ability = CharacterAbility.objects.get(
            character=character, ability=saving_throw.ability
        )

        modifier = character_ability.modifier
        new_value = (
            modifier + character.proficiency_bonus
            if saving_throw.proficiency
            else modifier
        )

        saving_throw.value = new_value
        saving_throw.save()

    return Response(
        {"detail": "Saving throws updated."},
        status=status.HTTP_200_OK,
    )
