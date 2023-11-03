from django.db import transaction, models
from rest_framework import serializers

from campaigns.models import (
    Character,
    CharacterMultiClass,
    CharacterAbility,
    CharacterSkill,
    PassiveSkill,
    SavingThrow,
    HitDice,
    SpellSlot,
)
from dnd_data.serializers import (
    UserSerializer,
    AlignmentSerializer,
    BackgroundSerializer,
    RaceSerializer,
)


# ------------------
# Character Creation
# ------------------
class CharacterMultiClassSerializer(serializers.ModelSerializer):
    character_class_name = serializers.StringRelatedField(source="character_class.name")

    class Meta:
        model = CharacterMultiClass
        fields = ("character_class", "character_class_name")


class CharacterAbilitySerializer(serializers.ModelSerializer):
    ability_name = serializers.StringRelatedField(source="ability.name")

    class Meta:
        model = CharacterAbility
        fields = ("ability", "ability_name", "score", "modifier")


class CharacterSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.StringRelatedField(source="skill.name")

    class Meta:
        model = CharacterSkill
        fields = ("skill", "skill_name", "value", "proficiency")


class PassiveSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.StringRelatedField(source="skill.name")

    class Meta:
        model = PassiveSkill
        fields = ("skill", "skill_name", "value", "proficiency")


class SavingThrowSerializer(serializers.ModelSerializer):
    ability_name = serializers.StringRelatedField(source="ability.name")

    class Meta:
        model = SavingThrow
        fields = ("ability", "ability_name", "value", "proficiency")


class HitDiceSerializer(serializers.ModelSerializer):
    dice_name = serializers.StringRelatedField(source="dice.name")

    class Meta:
        model = HitDice
        fields = ("dice", "dice_name", "max_qty", "actual_qty")


class SpellSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpellSlot
        fields = ("level", "max_slots", "remaining_slots")


class CharacterCreationSerializer(serializers.ModelSerializer):
    character_classes = CharacterMultiClassSerializer(many=True)
    character_abilities = CharacterAbilitySerializer(many=True)
    character_skills = CharacterSkillSerializer(many=True)
    passive_skills = PassiveSkillSerializer(many=True)
    saving_throws = SavingThrowSerializer(many=True)
    hit_dices = HitDiceSerializer(many=True)
    spell_slots = SpellSlotSerializer(many=True)

    class Meta:
        model = Character
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data):
        # Extract related objects data
        related_fields = {
            "character_classes": CharacterMultiClass,
            "character_abilities": CharacterAbility,
            "character_skills": CharacterSkill,
            "passive_skills": PassiveSkill,
            "saving_throws": SavingThrow,
            "hit_dices": HitDice,
            "spell_slots": SpellSlot,
        }
        related_data = {
            field: validated_data.pop(field) for field in related_fields.keys()
        }

        character = Character.objects.create(**validated_data)

        for field, model in related_fields.items():
            self._create_related_objects(
                model, "character", related_data[field], character
            )

        return character

    def _create_related_objects(
            self,
            model: models.Model,
            related_name: str,
            data_list: dict,
            instance: Character,
    ):
        objects_to_create = [
            model(**{related_name: instance, **data}) for data in data_list
        ]
        model.objects.bulk_create(objects_to_create)


# ------------------
# Character edit
# ------------------
class CharacterBasicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ["name", "race"]


# ------------------
# Other
# ------------------
class CharactersInCampaignListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = ["id", "name", "status"]


class CharacterSerializer(serializers.ModelSerializer):
    character_classes = CharacterMultiClassSerializer(many=True)
    race = RaceSerializer()
    background = BackgroundSerializer()
    alignment = AlignmentSerializer()
    player = UserSerializer()

    class Meta:
        model = Character
        fields = "__all__"
