from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from campaigns.constants import MODIFIER_MAP, PASSIVE_SKILLS
from campaigns.decorators import campaign_and_player_required
from campaigns.models import (
    CharacterAbility,
    CharacterSkill,
    SavingThrow,
    PassiveSkill,
    HitDice,
    SpellSlot,
    CharacterMultiClass,
)
from campaigns.serializers import (
    CharacterAbilitySerializer,
    CharacterSkillSerializer,
    PassiveSkillSerializer,
    SavingThrowSerializer,
    HitDiceSerializer,
    SpellSlotSerializer,
    CharacterBasicInfoSerializer,
    CharacterMultiClassSerializer,
)
from dnd_data.models import Skill, Ability, Dice, CharacterClass


@api_view(["PATCH"])
@campaign_and_player_required
def update_basic_info(request, character):
    data = request.data
    data["character"] = character.id

    serializer = CharacterBasicInfoSerializer(character, data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
@campaign_and_player_required
def update_character_multiclass(request, character):
    data = request.data
    response_data = []

    for item in data:
        character_class_instance = CharacterClass.objects.get(id=item["id"])
        item["character"] = character.id

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
@campaign_and_player_required
def update_character_abilities(request, character):
    data = request.data
    response_data = []

    for item in data:
        ability_instance = Ability.objects.get(id=item["ability"])
        item["character"] = character.id

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
@campaign_and_player_required
def update_character_skills(request, character):
    data = request.data
    response_data = []

    for item in data:
        skill_instance = Skill.objects.get(id=item["skill"])
        item["character"] = character.id

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
@campaign_and_player_required
def update_passive_skills(request, character):
    data = request.data
    response_data = []

    for item in data:
        skill_instance = Skill.objects.get(id=item["skill"])

        if skill_instance.name not in PASSIVE_SKILLS:
            return Response(
                {"message": f"{skill_instance.name} is not passive ability!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        item["character"] = character.id

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
@campaign_and_player_required
def update_saving_throws(request, character):
    data = request.data
    response_data = []

    for item in data:
        ability_instance = Ability.objects.get(id=item["ability"])

        item["character"] = character.id

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
@campaign_and_player_required
def update_hit_dices(request, character):
    data = request.data
    response_data = []

    for item in data:
        dice_instance = Dice.objects.get(id=item["dice"])

        item["character"] = character.id

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
@campaign_and_player_required
def update_spell_slots(request, character):
    data = request.data
    response_data = []

    for item in data:
        item["character"] = character.id

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
@campaign_and_player_required
def delete_character(request, character):
    character.status = "inactive"
    character.save()

    return Response(
        {"detail": "Campaign successfully set inactive."},
        status=status.HTTP_204_NO_CONTENT,
    )


@api_view(["PATCH"])
@campaign_and_player_required
def auto_update_character_abilities(request, character):
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
@campaign_and_player_required
def auto_update_character_skills(request, character):
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
@campaign_and_player_required
def auto_update_saving_throws(request, character):
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
