from django.apps import AppConfig
from django.conf import settings
from pokemontcgsdk import config

class App1Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app1"

    def ready(self):
        config.api_key = settings.TCG_API_KEY