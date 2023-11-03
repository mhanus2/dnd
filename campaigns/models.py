from django.db import models
from django.contrib.auth.models import User

from dnd_data.models import (
    CharacterClass,
    Race,
    Background,
    Alignment,
    Ability,
    Skill,
    Dice,
    Item,
    Spell,
)
from django.core.validators import MinValueValidator


# todo - zbrane

STATUS_CHOICES = [
    ("active", "Active"),
    ("inactive", "Inactive"),
    ("deceased", "Deceased"),
]


class Campaign(models.Model):
    name = models.CharField(max_length=200)
    dungeon_master = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    @property
    def session_count(self):
        return self.campaign_sessions.count()

    def __str__(self):
        return self.name


class Character(models.Model):
    # Basic Info
    name = models.CharField(max_length=100)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)

    background = models.ForeignKey(Background, on_delete=models.CASCADE)
    alignment = models.ForeignKey(Alignment, on_delete=models.CASCADE)

    # Health
    max_health = models.PositiveIntegerField(
        default=10, validators=[MinValueValidator(0)]
    )
    current_health = models.PositiveIntegerField(
        default=10, validators=[MinValueValidator(0)]
    )
    armor_class = models.PositiveIntegerField(default=10)

    # Efficiencies
    light_armor = models.BooleanField(default=False)
    middle_armor = models.BooleanField(default=False)
    heavy_armor = models.BooleanField(default=False)
    shields = models.BooleanField(default=False)

    # Magic
    magical_property = models.ForeignKey(Ability, on_delete=models.CASCADE, default=5)

    proficiency_bonus = models.PositiveIntegerField(default=0)

    inspiration = models.BooleanField(default=False)
    initiative = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="inactive")

    speed = models.PositiveIntegerField(default=0)

    notes = models.TextField(blank=True)

    player = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id and not self.speed:
            self.speed = self.race.speed

        Inventory.objects.get_or_create(character=self)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CharacterMultiClass(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="character_classes"
    )
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ("character", "character_class")
        verbose_name_plural = "Character MultiClasses"

    def __str__(self):
        return f"{self.character.name}'s {self.character_class.name}"


class CharacterAbility(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="character_abilities"
    )
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    modifier = models.IntegerField(default=0)

    class Meta:
        unique_together = ("character", "ability")
        verbose_name_plural = "Character abilities"

    def __str__(self):
        return f"{self.character.name}'s {self.ability.name}"


class CharacterSkill(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="character_skills"
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    proficiency = models.BooleanField(default=False)

    class Meta:
        unique_together = ("character", "skill")

    def __str__(self):
        return f"{self.character.name}'s {self.skill.name}"


class PassiveSkill(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="passive_skills"
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    proficiency = models.BooleanField(default=False)

    class Meta:
        unique_together = ("character", "skill")

    def __str__(self):
        return f"{self.character.name}'s {self.skill.name}"


class SavingThrow(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="saving_throws"
    )
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    proficiency = models.BooleanField(default=False)

    class Meta:
        unique_together = ("character", "ability")

    def __str__(self):
        return f"{self.character.name}'s {self.ability.name}"


class HitDice(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="hit_dices"
    )
    dice = models.ForeignKey(Dice, on_delete=models.CASCADE)
    max_qty = models.PositiveIntegerField(default=0)
    actual_qty = models.PositiveBigIntegerField(default=0)

    class Meta:
        unique_together = ("character", "dice")

    def __str__(self):
        return f"{self.character.name}'s {self.dice.name}"


# ----------
# Inventory
# ----------
class Inventory(models.Model):
    character = models.OneToOneField(
        Character, on_delete=models.CASCADE, related_name="inventory"
    )

    class Meta:
        verbose_name_plural = "Inventories"

    def __str__(self) -> str:
        return f"Inventory of {self.character}"


class InventoryItem(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    note = models.TextField(blank=True)
    qty = models.PositiveSmallIntegerField(default=1)
    attunement = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.qty}x {self.item.name}"


# ------
# Spells
# ------
class CharacterSpell(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    spell = models.ForeignKey(Spell, on_delete=models.CASCADE)
    character_class_relation = models.ForeignKey(
        CharacterMultiClass, on_delete=models.CASCADE, related_name="known_spells"
    )
    prepared = models.BooleanField(default=False)
    note = models.TextField(blank=True)

    class Meta:
        unique_together = ["character", "spell"]


class SpellSlot(models.Model):
    character = models.ForeignKey(
        Character, on_delete=models.CASCADE, related_name="spell_slots"
    )
    level = models.PositiveIntegerField()
    max_slots = models.PositiveIntegerField(default=0)
    remaining_slots = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("character", "level")

    def __str__(self):
        return f"{self.character.name}'s Level {self.level} Spell Slots"


# -------
# Session
# -------
class Session(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name='campaign_sessions')
    name = models.CharField(max_length=200)
    date = models.DateField()

    @property
    def character_count(self):
        return self.session_characters.count()

    def __str__(self):
        return self.name


class SessionCharacter(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='sessions_characters')
    character = models.ForeignKey(Character, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['session', 'character']

    def __str__(self):
        return f"{self.character.name} in {self.session.name}"
