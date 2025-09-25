from django.db import models
from vendas.models.models_venda import Venda
from core.models import FormaPagamento
class VendaParcela(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='parcelas_venda',)
    
    numero_parcela = models.PositiveIntegerField(
        verbose_name='Número da Parcela'
    )

    quantidade_parcelas = models.PositiveIntegerField(
        verbose_name='Quantidade Total de Parcelas'
    )

    data_vencimento = models.DateField(
        verbose_name='Data de Vencimento da Parcela'
    )

    valor_parcela = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor da Parcela'
    )
    forma_pagamento = models.ForeignKey(
        FormaPagamento,
        on_delete=models.PROTECT,
        related_name='parcelas_venda'
    )
    situacao = models.CharField(
        max_length=1,
        choices=[
            ('A', 'Aberta'),
            ('P', 'Paga'),
            ('C', 'Cancelada')
        ],
        default='A',
        verbose_name='Situação'
    )

    class Meta:
        verbose_name = 'Parcela da Venda'
        verbose_name_plural = 'Parcelas das Vendas'
        ordering = ['venda', 'numero_parcela']

    def __str__(self):
        return f"Venda {self.venda_id} - Parcela {self.numero_parcela}/{self.quantidade_parcelas}"
