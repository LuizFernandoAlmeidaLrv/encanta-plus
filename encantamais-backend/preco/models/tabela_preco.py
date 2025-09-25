from django.db import models
from django.conf import settings


class TabelaPreco(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(blank=True, null=True)
    situacao = models.CharField(max_length=1, choices=[('A', 'Ativa'), ('I', 'Inativa')], default='A')
    data_criacao = models.DateField(auto_now_add=True)
    usuario_criacao = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
   

    def __str__(self):
        return self.nome
