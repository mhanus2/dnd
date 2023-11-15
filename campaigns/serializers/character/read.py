from rest_framework import serializers

from campaigns.models import Character
from campaigns.serializers.character.shared import (
    SerializerCharacterMultiClass,
    SerializerCharacterAbility,
    SerializerCharacterSkill,
    SerializerPassiveSkill,
    SerializerSavingThrow,
    SerializerHitDice,
    SerializerSpellSlot,
    SerializerCharacterSpell
)
from dnd_data.serializers import (
    SerializerUser,
    SerializerAlignment,
    SerializerBackground,
    SerializerRace,
)


class SerializerCharacter(serializers.ModelSerializer):
    character_classes = SerializerCharacterMultiClass(many=True)
    character_abilities = SerializerCharacterAbility(many=True)
    character_skills = SerializerCharacterSkill(many=True)
    passive_skills = SerializerPassiveSkill(many=True)
    saving_throws = SerializerSavingThrow(many=True)
    hit_dices = SerializerHitDice(many=True)
    spell_slots = SerializerSpellSlot(many=True)
    character_spells = SerializerCharacterSpell(many=True)
    race = SerializerRace()
    background = SerializerBackground()
    alignment = SerializerAlignment()
    player = SerializerUser()

    class Meta:
        model = Character
        fields = "__all__"  # todo - vyspecifikovat, co vše odesílat


class SerializerCharactersInCampaignList(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = "__all__"  # todo - vyspecifikovat, co vše odesílat
