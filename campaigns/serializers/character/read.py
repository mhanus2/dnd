from rest_framework import serializers

from campaigns.models import Character
from campaigns.serializers.character.shared import (
    CharacterMultiClassSerializer,
    CharacterAbilitySerializer,
    CharacterSkillSerializer,
    PassiveSkillSerializer,
    SavingThrowSerializer,
    HitDiceSerializer,
    SpellSlotSerializer,
    CharacterSpellSerializer
)
from dnd_data.serializers import (
    UserSerializer,
    AlignmentSerializer,
    BackgroundSerializer,
    RaceSerializer,
)


class CharacterSerializer(serializers.ModelSerializer):
    character_classes = CharacterMultiClassSerializer(many=True)
    character_abilities = CharacterAbilitySerializer(many=True)
    character_skills = CharacterSkillSerializer(many=True)
    passive_skills = PassiveSkillSerializer(many=True)
    saving_throws = SavingThrowSerializer(many=True)
    hit_dices = HitDiceSerializer(many=True)
    spell_slots = SpellSlotSerializer(many=True)
    character_spells = CharacterSpellSerializer(many=True)
    race = RaceSerializer()
    background = BackgroundSerializer()
    alignment = AlignmentSerializer()
    player = UserSerializer()

    class Meta:
        model = Character
        fields = "__all__"  # todo - vyspecifikovat, co vše odesílat


class CharactersInCampaignListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Character
        fields = "__all__"  # todo - vyspecifikovat, co vše odesílat
