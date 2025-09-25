from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    nome_completo = models.CharField(max_length=150)
    tipo = models.CharField(
        max_length=20,
        choices=[
            ('ADMIN', 'Administrador'),
            ('VENDEDOR', 'Vendedor'),
            ('CAIXA', 'Caixa'),
        ],
        default='VENDEDOR'
    )

    def __str__(self):
        return self.username
