from django.db import models
from django.contrib.auth.models import User

from dnd_data.models import CharacterClass, Race, Background, Alignment


# todo - počet session, počet hráčů, datum poslední schůzky    

STATUS_CHOICES = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('deceased', 'Deceased'),
)


class Campaign(models.Model):
    name = models.CharField(max_length=200)
    dungeon_master = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Character(models.Model):
    name = models.CharField(max_length=200)
    character_class = models.ForeignKey(CharacterClass, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    background = models.ForeignKey(Background, on_delete=models.CASCADE)
    alignment = models.ForeignKey(Alignment, on_delete=models.CASCADE)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='inactive')
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Session(models.Model):
    name = models.CharField(max_length=200)



    