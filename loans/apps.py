from django.apps import AppConfig
from typing import Literal


class LoansConfig(AppConfig):
    default_auto_field: str = 'django.db.models.BigAutoField'
    name: str = 'loans'
