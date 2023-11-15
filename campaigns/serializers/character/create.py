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
    CharacterSpell
)
from campaigns.serializers.character.shared import (
    SerializerCharacterMultiClass,
    SerializerCharacterAbility,
    SerializerCharacterSkill,
    SerializerPassiveSkill,
    SerializerSavingThrow,
    SerializerHitDice,
    SerializerSpellSlot,
    SerializerCharacterSpell,
)


class SerializerCharacterCreation(serializers.ModelSerializer):
    character_classes = SerializerCharacterMultiClass(many=True)
    character_abilities = SerializerCharacterAbility(many=True)
    character_skills = SerializerCharacterSkill(many=True)
    passive_skills = SerializerPassiveSkill(many=True)
    saving_throws = SerializerSavingThrow(many=True)
    hit_dices = SerializerHitDice(many=True)
    spell_slots = SerializerSpellSlot(many=True)
    character_spells = SerializerCharacterSpell(many=True)

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
            "character_spells": CharacterSpell
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
