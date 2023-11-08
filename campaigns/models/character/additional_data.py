from django.db import models


class CharacterMultiClass(models.Model):
    character = models.ForeignKey(
        "campaigns.Character",
        on_delete=models.CASCADE,
        related_name="character_classes",
    )
    character_class = models.ForeignKey(
        "dnd_data.CharacterClass", on_delete=models.CASCADE
    )
    level = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ("character", "character_class")
        verbose_name_plural = "Character MultiClasses"

    def __str__(self):
        return f"{self.character.name}'s {self.character_class.name}"


class CharacterAbility(models.Model):
    character = models.ForeignKey(
        "campaigns.Character",
        on_delete=models.CASCADE,
        related_name="character_abilities",
    )
    ability = models.ForeignKey("dnd_data.Ability", on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    modifier = models.IntegerField(default=0)

    class Meta:
        unique_together = ("character", "ability")
        verbose_name_plural = "Character abilities"

    def __str__(self):
        return f"{self.character.name}'s {self.ability.name}"


class CharacterSkill(models.Model):
    character = models.ForeignKey(
        "campaigns.Character", on_delete=models.CASCADE, related_name="character_skills"
    )
    skill = models.ForeignKey("dnd_data.Skill", on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    proficiency = models.BooleanField(default=False)

    class Meta:
        unique_together = ("character", "skill")

    def __str__(self):
        return f"{self.character.name}'s {self.skill.name}"


class PassiveSkill(models.Model):
    character = models.ForeignKey(
        "campaigns.Character", on_delete=models.CASCADE, related_name="passive_skills"
    )
    skill = models.ForeignKey("dnd_data.Skill", on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    proficiency = models.BooleanField(default=False)

    class Meta:
        unique_together = ("character", "skill")

    def __str__(self):
        return f"{self.character.name}'s {self.skill.name}"


class SavingThrow(models.Model):
    character = models.ForeignKey(
        "campaigns.Character", on_delete=models.CASCADE, related_name="saving_throws"
    )
    ability = models.ForeignKey("dnd_data.Ability", on_delete=models.CASCADE)
    value = models.IntegerField(default=0)
    proficiency = models.BooleanField(default=False)

    class Meta:
        unique_together = ("character", "ability")

    def __str__(self):
        return f"{self.character.name}'s {self.ability.name}"


class HitDice(models.Model):
    character = models.ForeignKey(
        "campaigns.Character", on_delete=models.CASCADE, related_name="hit_dices"
    )
    dice = models.ForeignKey("dnd_data.Dice", on_delete=models.CASCADE)
    max_qty = models.PositiveIntegerField(default=0)
    actual_qty = models.PositiveBigIntegerField(default=0)

    class Meta:
        unique_together = ("character", "dice")

    def __str__(self):
        return f"{self.character.name}'s {self.dice.name}"


class CharacterSpell(models.Model):
    character = models.ForeignKey(
        "campaigns.Character", on_delete=models.CASCADE, related_name="character_spells"
    )
    spell = models.ForeignKey("dnd_data.Spell", on_delete=models.CASCADE)
    character_class_relation = models.ForeignKey(
        "campaigns.CharacterMultiClass",
        on_delete=models.CASCADE,
        related_name="known_spells",
    )
    prepared = models.BooleanField(default=False)
    note = models.TextField(blank=True)

    class Meta:
        unique_together = ["character", "spell"]


class SpellSlot(models.Model):
    character = models.ForeignKey(
        "campaigns.Character", on_delete=models.CASCADE, related_name="spell_slots"
    )
    level = models.PositiveIntegerField()
    max_slots = models.PositiveIntegerField(default=0)
    remaining_slots = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("character", "level")

    def __str__(self):
        return f"{self.character.name}'s Level {self.level} Spell Slots"


class CharacterWeapon(models.Model):
    character = models.ForeignKey("campaigns.Character", on_delete=models.CASCADE)
    weapon = models.ForeignKey("dnd_data.Weapon", on_delete=models.CASCADE)


class Inventory(models.Model):
    character = models.OneToOneField(
        "campaigns.Character", on_delete=models.CASCADE, related_name="inventory"
    )

    class Meta:
        verbose_name_plural = "Inventories"

    def __str__(self) -> str:
        return f"Inventory of {self.character}"


class InventoryItem(models.Model):
    inventory = models.ForeignKey("campaigns.Inventory", on_delete=models.CASCADE)
    item = models.ForeignKey("dnd_data.Item", on_delete=models.CASCADE)
    note = models.TextField(blank=True)
    qty = models.PositiveSmallIntegerField(default=1)
    attunement = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.qty}x {self.item.name}"
