from django.db import models
from rest_framework import serializers
from produtos.models.categoria import Categoria
from core.models.fornecedor import Fornecedor
from produtos.models.unidade_medida import UnidadeMedida
from django.utils import timezone



class Produto(models.Model):
    
    codigo = models.CharField(primary_key=True, max_length=20)  # Ex: P001
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    tamanho = models.ForeignKey(UnidadeMedida, to_field='codigo', on_delete=models.PROTECT)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True, blank=True)
    codigo_agrupamento = models.CharField(max_length=20, blank=True, null=True)

    cor = models.CharField(max_length=50, blank=True, null=True)
   
    custo_ultimo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    custo_medio = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)

    ativo = models.BooleanField(default=True)

    criado_em = models.DateTimeField(default=timezone.now)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
            return f"{self.codigo} - {self.nome}"
    
    