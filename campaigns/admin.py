from django.contrib import admin
from .models import (
    Campaign,
    Character,
    CharacterAbility,
    CharacterSkill,
    PassiveSkill,
    SavingThrow,
    HitDice,
    SpellSlot,
)


class CharacterAbilityInline(admin.TabularInline):
    model = CharacterAbility
    extra = 1


class CharacterSkillInline(admin.TabularInline):
    model = CharacterSkill
    extra = 1


class PassiveSkillInline(admin.TabularInline):
    model = PassiveSkill
    extra = 1


class SavingThrowInline(admin.TabularInline):
    model = SavingThrow
    extra = 1


class HitDiceInline(admin.TabularInline):
    model = HitDice
    extra = 1


class SpellSlotInline(admin.TabularInline):
    model = SpellSlot
    extra = 1


class CharacterAdmin(admin.ModelAdmin):
    inlines = [
        CharacterAbilityInline,
        CharacterSkillInline,
        SavingThrowInline,
        PassiveSkillInline,
        HitDiceInline,
        SpellSlotInline,
    ]


admin.site.register(Campaign)
admin.site.register(CharacterAbility)
admin.site.register(CharacterSkill)
admin.site.register(Character, CharacterAdmin)
