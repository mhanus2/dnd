from django.db import models


# todo - Pridat description a pak i do serializeru

class Session(models.Model):
    campaign = models.ForeignKey(
        "campaigns.Campaign", on_delete=models.CASCADE, related_name="campaign_sessions"
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()

    @property
    def character_count(self):
        return self.session_characters.count()

    def __str__(self):
        return self.name


class SessionCharacter(models.Model):
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name="session_characters"
    )
    character = models.ForeignKey("campaigns.Character", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["session", "character"]

    def __str__(self):
        return f"{self.character.name} in {self.session.name}"
