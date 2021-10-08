"""This apps.py contain PollsConfig class."""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """PollsConfig class contain auto fields and name of app."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
