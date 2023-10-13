from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    Character,
    CharacterAbility,
    CharacterSkill,
    SavingThrow,
    PassiveSkill,
)
from dnd_data.models import Ability, Skill


PASSIVE_SKILLS = ["Athletics", "Acrobatics", "Stealth", "Insight", "Perception"]


@receiver(post_save, sender=Character)
def create_character_stats(sender, instance, created, **kwargs):
    if created:
        abilities = Ability.objects.all()
        for ability in abilities:
            CharacterAbility.objects.get_or_create(character=instance, ability=ability)
            SavingThrow.objects.get_or_create(character=instance, ability=ability)

        skills = Skill.objects.all()
        for skill in skills:
            CharacterSkill.objects.get_or_create(
                character=instance,
                skill=skill,
            )
            if skill.name in PASSIVE_SKILLS:
                PassiveSkill.objects.get_or_create(
                    character=instance,
                    skill=skill,
                )
