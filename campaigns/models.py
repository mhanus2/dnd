from django.db import models
from django.contrib.auth.models import User

from characters.models import Character

# todo - počet session, počet hráčů, datum poslední schůzky    

class Session(models.Model):
    name = models.CharField(max_length=200)
    

class Campaign(models.Model):
    name = models.CharField(max_length=200)
    dungeon_master = models.ForeignKey(User, on_delete=models.CASCADE)
    characters = models.ManyToManyField(Character, related_name='campaigns', blank=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    @property
    def number_of_characters(self):
        return self.characters.count()
    