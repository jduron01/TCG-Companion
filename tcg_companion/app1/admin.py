from django.contrib import admin
from app1.models import CardData, Deck, DeckEntry, Collection, CollectionEntry, GeminiStrategy

admin.site.register(CardData)
admin.site.register(Deck)
admin.site.register(DeckEntry)
admin.site.register(Collection)
admin.site.register(CollectionEntry)
admin.site.register(GeminiStrategy)