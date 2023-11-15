from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

# todo - inventar vytvorit po vytvoreni postavy
# todo - magical property - empty u nemagickych postav?
# todo - so zachrany - jak to nazvat?

STATUS_CHOICES = [
    ("active", "Active"),
    ("inactive", "Inactive"),
    ("deceased", "Deceased"),
]


class Character(models.Model):
    # Basic Info
    name = models.CharField(max_length=100)
    race = models.ForeignKey("dnd_data.Race", on_delete=models.CASCADE)

    background = models.ForeignKey("dnd_data.Background", on_delete=models.CASCADE)
    alignment = models.ForeignKey("dnd_data.Alignment", on_delete=models.CASCADE)

    # Health
    max_health = models.PositiveIntegerField(
        default=10, validators=[MinValueValidator(0)]
    )
    current_health = models.PositiveIntegerField(
        default=10, validators=[MinValueValidator(0)]
    )
    armor_class = models.PositiveIntegerField(default=10)

    # Attributes
    proficiency_bonus = models.PositiveIntegerField(default=0)
    inspiration = models.BooleanField(default=False)
    initiative = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="inactive")
    speed = models.PositiveIntegerField(default=0)

    # Efficiencies
    light_armor = models.BooleanField(default=False)
    middle_armor = models.BooleanField(default=False)
    heavy_armor = models.BooleanField(default=False)
    shields = models.BooleanField(default=False)

    # Magic
    magical_property = models.ForeignKey(
        "dnd_data.Ability", on_delete=models.CASCADE, default=5
    )
    magical_attack_bonus = models.SmallIntegerField(default=0)
    alchemy_jug = models.SmallIntegerField(default=0)

    notes = models.TextField(blank=True)

    player = models.ForeignKey(User, on_delete=models.CASCADE)
    campaign = models.ForeignKey("campaigns.Campaign", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
