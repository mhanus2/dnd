from django.db import models

# todo - zjistit co vše je potřeba u spellů
# todo - zjistit co vše je potřeba u zbraní


class Race(models.Model):
    name = models.CharField(max_length=200)
    speed = models.IntegerField(default=6)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def to_json(self):
        json_data = {
            "id": self.id,
            "name": self.name,
            "speed": self.speed,
            "created": self.created,
        }
        return json_data


class CharacterClass(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Character Classes"

    def to_json(self):
        json_data = {
            "id": self.id,
            "name": self.name,
            "created": self.created,
        }
        return json_data


class Background(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def to_json(self):
        json_data = {
            "id": self.id,
            "name": self.name,
            "created": self.created,
        }
        return json_data


class Alignment(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def to_json(self):
        json_data = {
            "id": self.id,
            "name": self.name,
            "created": self.created,
        }
        return json_data


class Ability(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Abilities"


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


class Weapon(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class SpellType(models.Model):
    name = models.CharField(max_length=10)

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
    type = models.ForeignKey(SpellType, on_delete=models.CASCADE, related_name="spells")
    school = models.ForeignKey(
        SpellSchool, on_delete=models.CASCADE, related_name="spells"
    )
    casting_time = models.CharField(max_length=10)
    range = models.CharField(max_length=10)
    duration = models.CharField(max_length=25)
    components = models.ManyToManyField(SpellComponent, related_name="spells")

    def __str__(self) -> str:
        return self.name
