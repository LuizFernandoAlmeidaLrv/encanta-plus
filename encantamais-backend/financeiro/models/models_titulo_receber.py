from django.db import models
from core.models.cliente import Cliente
from vendas.models.models_venda import Venda
from core.models import FormaPagamento
from django.db.models.signals import post_save
from django.dispatch import receiver

SITUACAO_TITULO = (
    ('A', 'Aberto'),
    ('B', 'Baixado'),
    ('C', 'Cancelado'),
)

class TituloReceber(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='titulos')
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    valor_aberto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    forma_pagamento = models.ForeignKey(
        FormaPagamento,
        on_delete=models.PROTECT,
        related_name='titulos_receber'
    )
    data_movimento = models.DateField(auto_now_add=True)
    data_vencimento = models.DateField()
    data_recebimento = models.DateField(blank=True, null=True)
    situacao = models.CharField(max_length=1, choices=SITUACAO_TITULO, default='A')
    observacao = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Título #{self.id} - {self.cliente.nome}'

