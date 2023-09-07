from django.db import models


class Character(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    character_class = models.CharField(max_length=200, blank=True, null=True)
    level = models.CharField(max_length=200, blank=True, null=True)
    race = models.CharField(max_length=200, blank=True, null=True)
    background = models.CharField(max_length=200, blank=True, null=True)
    alignment = models.CharField(max_length=200, blank=True, null=True)
    player_name = models.CharField(max_length=200, blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    