from rest_framework import serializers

from campaigns.models import (
    CharacterMultiClass,
    CharacterAbility,
    CharacterSkill,
    PassiveSkill,
    SavingThrow,
    HitDice,
    SpellSlot,
    CharacterSpell
)


class CharacterMultiClassSerializer(serializers.ModelSerializer):
    character_class_name = serializers.StringRelatedField(source="character_class.name")

    class Meta:
        model = CharacterMultiClass
        fields = ("character_class", "character_class_name", "level")


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


class CharacterSpellSerializer(serializers.ModelSerializer):
    spell_name = serializers.StringRelatedField(source="spell.name")
    character_class_relation = CharacterMultiClassSerializer()

    class Meta:
        model = CharacterSpell
        fields = ("spell", "spell_name", "character_class_relation", "prepared", "note")
