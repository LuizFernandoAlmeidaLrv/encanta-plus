from django.db import models
from decimal import Decimal
from datetime import timedelta
from core.models.cliente import Cliente
from core.models import FormaPagamento, Usuario
from produtos.models.produto import Produto
from suprimentos.models.deposito  import Deposito

TIPOS_VENDA = (
    ('AV', 'À Vista'),
    ('AP', 'A Prazo'),
)

SITUACOES_VENDA = (
    ('DI', 'Digitada'),
    ('FE', 'Fechada'),
    ('CA', 'Cancelada'),
    ('EX', 'Excluída'),
    ('LI', 'Liberada'),
    ('DE', 'Devolvida'),
)



class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    data_venda = models.DateTimeField(auto_now_add=True)
    data_liberacao = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=2, choices=TIPOS_VENDA)
    forma_pagamento = models.ForeignKey(
        FormaPagamento,
        on_delete=models.PROTECT,
        related_name='vendas'
    )
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    valor_entrada = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    quantidade_parcelas = models.IntegerField(default=1)
    situacao = models.CharField(max_length=2, choices=SITUACOES_VENDA, default='DI')
    observacao = models.TextField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.PROTECT)

    def __str__(self):
        return f'Venda #{self.id} - {self.cliente.nome}'




class VendaItem(models.Model):
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT)
    quantidade = models.DecimalField(max_digits=8, decimal_places=2)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    deposito = models.ForeignKey(Deposito, on_delete=models.PROTECT, null=True, blank=True)
    @property
    def subtotal(self):
        return self.quantidade * self.valor_unitario
