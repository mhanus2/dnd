from django.contrib import admin
from .models import Race, CharacterClass, Background, Alignment, Ability, Skill, Dice


class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'ability']


admin.site.register(Race)
admin.site.register(CharacterClass)
admin.site.register(Background)
admin.site.register(Alignment)
admin.site.register(Ability)
admin.site.register(Dice)
admin.site.register(Skill, SkillAdmin)
