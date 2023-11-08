from django.db import models
from django.contrib.auth.models import User


class Campaign(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    dungeon_master = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def session_count(self):
        return self.campaign_sessions.count()

    def __str__(self):
        return self.name
