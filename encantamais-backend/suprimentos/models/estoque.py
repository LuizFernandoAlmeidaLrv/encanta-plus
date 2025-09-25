# suprimentos/models/estoque.py

from django.db import models
from produtos.models.produto import Produto
from suprimentos.models.deposito import Deposito

class Estoque(models.Model):
    produto = models.ForeignKey(
        Produto, on_delete=models.PROTECT, to_field='codigo'
    )
    deposito = models.ForeignKey(
        Deposito, on_delete=models.PROTECT, to_field='codigo'
    )
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('produto', 'deposito')

    def __str__(self):
        return f"{self.produto.codigo} - {self.deposito.codigo}: {self.saldo}"
