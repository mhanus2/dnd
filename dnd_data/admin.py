from django.contrib import admin
from .models import Race, CharacterClass, Background, Alignment, Ability, Skill, Dice, Tag, Item, Spell, SpellSchool, SpellComponent, Weapon, DamageType

class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'ability']


admin.site.register(Race)
admin.site.register(CharacterClass)
admin.site.register(Background)
admin.site.register(Alignment)
admin.site.register(Ability)
admin.site.register(Dice)
admin.site.register(Tag)
admin.site.register(Item)
admin.site.register(Weapon)
admin.site.register(Spell)
admin.site.register(SpellSchool)
admin.site.register(SpellComponent)
admin.site.register(DamageType)

admin.site.register(Skill, SkillAdmin)
