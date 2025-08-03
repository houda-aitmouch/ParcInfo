from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    username_validator = RegexValidator(
        regex=r'^[\w.@+\- ]+$',  # autorise les espaces
        message="Ce champ peut contenir des lettres, chiffres, @/./+/-/_ et espaces."
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        help_text="Requis. 150 caractères max. Lettres, chiffres, @/./+/-/_ et espaces autorisés.",
        error_messages={
            "unique": "Un utilisateur avec ce nom existe déjà.",
        },
    )

    def __str__(self):
        return self.username