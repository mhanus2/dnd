from django.db import models
from races.models import Race


class Character(models.Model):
    name = models.CharField(max_length=200)
    character_class = models.CharField(max_length=200)
    level = models.IntegerField(default=1)
    race = models.ForeignKey(Race, on_delete=models.SET_NULL, null=True, blank=True)
    background = models.CharField(max_length=200, blank=True, null=True)
    alignment = models.CharField(max_length=200, blank=True, null=True)
    player_name = models.CharField(max_length=200, blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    


    