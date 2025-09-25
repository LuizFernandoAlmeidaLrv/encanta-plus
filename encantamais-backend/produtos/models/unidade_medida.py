# produtos/models/unidade_medida.py

from django.db import models

class UnidadeMedida(models.Model):
    codigo = models.CharField(max_length=10, primary_key=True)  # Ex: UN, KG, CX
    nome = models.CharField(max_length=50)                      # Ex: 'Unidade', 'Quilograma'

    def __str__(self):
        return f"{self.codigo} - {self.nome}"
