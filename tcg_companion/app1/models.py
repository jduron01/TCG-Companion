from django.db import models
from django.contrib.auth.models import User

class CardData(models.Model):
    id = models.CharField(primary_key=True, max_length=20)
    name = models.CharField(max_length=30)
    number = models.IntegerField()
    type = models.CharField(max_length=10)
    image = models.URLField()
    prices = models.JSONField(null=True, blank=True, default=dict)

    # Pokemon-specific data
    hp = models.IntegerField(null=True, blank=True)
    types = models.JSONField(null=True, blank=True, default=list)
    abilities = models.JSONField(null=True, blank=True, default=dict)
    attacks = models.JSONField(null=True, blank=True, default=dict)
    weaknesses = models.JSONField(null=True, blank=True, default=dict)
    resistances = models.JSONField(null=True, blank=True, default=list)
    retreat = models.IntegerField(null=True, blank=True, default=1)

    # Trainer- and energy-specific data
    rules = models.JSONField(null=True, blank=True, default=list)

    class Meta:
        unique_together = ("name", "number")

class Deck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class DeckEntry(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name="entries")
    card = models.ForeignKey(CardData, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    class Meta:
        unique_together = ("deck", "card")

class Collection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class CollectionEntry(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name="entries")
    card = models.ForeignKey(CardData, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    class Meta:
        unique_together = ("collection", "card")

class GeminiStrategy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name="strategies")
    request = models.TextField()
    response = models.TextField()