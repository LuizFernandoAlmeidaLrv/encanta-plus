# suprimentos/models/deposito.py

from django.db import models

class Deposito(models.Model):
    codigo = models.CharField(primary_key=True, max_length=10)  # Ex: E001
    nome = models.CharField(max_length=100)                # Ex: "Loja Matriz"
    descricao = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"
