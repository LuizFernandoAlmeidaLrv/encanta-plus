# suprimentos/models/nota_fiscal_entrada_item.py

from django.db import models
from produtos.models.produto import Produto
from suprimentos.models.nota_fiscal_entrada import NotaFiscalEntrada
from suprimentos.models.deposito import Deposito

class NotaFiscalEntradaItem(models.Model):
    nota_fiscal = models.ForeignKey(NotaFiscalEntrada, on_delete=models.CASCADE, related_name='itens')
    produto = models.ForeignKey(Produto, on_delete=models.PROTECT, to_field='codigo')  # <-- aqui
    deposito = models.ForeignKey(Deposito, on_delete=models.PROTECT, to_field='codigo')  # <-- aqui
    quantidade = models.DecimalField(max_digits=10, decimal_places=2)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    valor_total = models.DecimalField(max_digits=12, decimal_places=2)
    
    percentual_frete = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # <- Aqui
    valor_frete_aplicado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    custo_unitario_calculado = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    aplicar_custo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.produto.nome} x {self.quantidade}"
