from django.db import models


class Race(models.Model):
    name = models.CharField(max_length=200)
    speed = models.IntegerField(default=30)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def to_json(self):
        json_data = {
            'id': self.id,
            'name': self.name,
            'speed': self.speed,
            'created': self.created,
        }
        return json_data
    

from django.db import models


class CharacterClass(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Character Classes'

    def to_json(self):
        json_data = {
            'id': self.id,
            'name': self.name,
            'created': self.created,
        }
        return json_data
    

class Background(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def to_json(self):
        json_data = {
            'id': self.id,
            'name': self.name,
            'created': self.created,
        }
        return json_data
    
class Alignment(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def to_json(self):
        json_data = {
            'id': self.id,
            'name': self.name,
            'created': self.created,
        }
        return json_data
    