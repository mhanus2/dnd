from django.db import models


class Campaign(models.Model):
    name = models.CharField(max_length=200)
    dungeon_master = models.CharField(max_length=200)
    characters = models.TextField(null=True, blank=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    