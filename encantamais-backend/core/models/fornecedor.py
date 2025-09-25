from django.db import models
from django.utils.timezone import now

# Modelo para Fornecedor
class Fornecedor(models.Model):
    cnpj_cpf = models.CharField(max_length=18)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True)
    numero = models.CharField(max_length=10, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    cep = models.CharField(max_length=10, blank=True)
    data_cadastro = models.DateTimeField(default=now)
    def __str__(self):
        return self.nome
