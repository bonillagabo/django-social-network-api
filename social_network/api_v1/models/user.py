from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )

    # Anula los campos 'groups' y 'user_permissions' para evitar conflictos con el modelo built-in 'user' de Django
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="api_v1_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="api_v1_user_permissions",
        blank=True,
    )

    def set_password(self, raw_password):
        """Encripta la contraseña usando el método de Django"""
        super().set_password(raw_password)
