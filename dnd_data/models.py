from django.db import models



class Race(models.Model):
    name = models.CharField(max_length=200)
    speed = models.IntegerField(default=6)

    def __str__(self):
        return self.name


class CharacterClass(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "Character Classes"

    def __str__(self):
        return self.name


class Background(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Alignment(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Ability(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Abilities"

    def __str__(self):
        return self.name


class Skill(models.Model):
    name = models.CharField(max_length=100)
    ability = models.ForeignKey(
        Ability, on_delete=models.CASCADE, related_name="ability_skills"
    )

    def __str__(self):
        return self.name


class Dice(models.Model):
    name = models.CharField(max_length=5)
    value = models.IntegerField(default=6)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    value = models.PositiveIntegerField()
    tags = models.ManyToManyField(Tag, related_name="tags")
    allowed_characters = models.ManyToManyField(
        "campaigns.Character", related_name="accessible_items", blank=True
    )

    def __str__(self) -> str:
        return self.name


class DamageType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Weapon(models.Model):
    name = models.CharField(max_length=50)
    damage_dice_count = models.PositiveSmallIntegerField(default=1)
    damage_dice = models.ForeignKey(Dice, on_delete=models.CASCADE)
    damage_type = models.ForeignKey(DamageType, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class SpellSchool(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class SpellComponent(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name


class Spell(models.Model):
    name = models.CharField(max_length=50)
    level = models.PositiveSmallIntegerField(default=1)
    school = models.ForeignKey(
        SpellSchool, on_delete=models.CASCADE, related_name="spells"
    )
    casting_time = models.CharField(max_length=10)
    range = models.CharField(max_length=10)
    duration = models.CharField(max_length=25)
    components = models.ManyToManyField(SpellComponent, related_name="spells")

    def __str__(self) -> str:
        return self.name
