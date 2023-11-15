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
    CharacterMultiClass,
    Inventory,
    InventoryItem,
    CharacterSpell,
    Session,
    SessionCharacter,
    CharacterWeapon
)


# -----------------
# Character inlines
# -----------------
class CharacterMultiClassInline(admin.TabularInline):
    model = CharacterMultiClass
    extra = 1


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


class InventoryInline(admin.TabularInline):
    model = Inventory
    extra = 1


class CharacterSpellInline(admin.TabularInline):
    model = CharacterSpell
    extra = 1

class CharacterWeaponInline(admin.TabularInline):
    model = CharacterWeapon
    extra = 1


# -----------------
# Inventory inlines
# -----------------
class InventoryItemInline(admin.TabularInline):
    model = InventoryItem
    extra = 1


# ----------
# ModelAdmin
# ----------
class CharacterAdmin(admin.ModelAdmin):
    inlines = [
        CharacterMultiClassInline,
        CharacterAbilityInline,
        CharacterSkillInline,
        SavingThrowInline,
        PassiveSkillInline,
        HitDiceInline,
        SpellSlotInline,
        CharacterSpellInline,
        CharacterWeaponInline
    ]


class InventoryAdmin(admin.ModelAdmin):
    inlines = [InventoryItemInline]


admin.site.register(Campaign)
admin.site.register(Session)
admin.site.register(SessionCharacter)
admin.site.register(CharacterAbility)
admin.site.register(CharacterSkill)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Inventory, InventoryAdmin)
